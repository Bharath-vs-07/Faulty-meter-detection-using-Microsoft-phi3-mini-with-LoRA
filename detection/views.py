from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponse
from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer
import torch
import pandas as pd
import random
import os
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST


# Load the model and tokenizer (only load once)
model = AutoPeftModelForCausalLM.from_pretrained(r"model", load_in_4bit=True)
tokenizer = AutoTokenizer.from_pretrained(r"model")

alpaca_prompt = """Below is an input that describes the context. Write a response that appropriately completes the request.
### Input:
{}
### Response:
{}"""

root_cause_mapping = {
    "Low Tampering": ["Meter Bypass", "Incorrect Calibration", "Firmware Manipulation", "Magnetic Interference", "Bypass of Meter", "Reverse Metering"],
    "High Tampering": ["Meter Bypass", "Incorrect Calibration", "Firmware Manipulation", "Magnetic Interference", "Bypass of Meter", "Reverse Metering"],
    "Normal": None
}

def generate_inference_input(row):
    inp = (
        f"Daily Consumption (kWh): {row['Daily Consumption (kWh)']}, "
        f"Peak Load (kWh): {row['Peak Load (kWh)']}, "
        f"Baseline Consumption (kWh): {row['Baseline Consumption (kWh)']}, "
        f"Seasonal Trend: {row['Seasonal Trend']}, "
        f"Autocorrelation: {row['Autocorrelation']}, "
        f"Moving Average (kWh): {row['Moving Average (kWh)']}, "
        f"Meter vs. Billing (kWh): {row['Meter vs. Billing (kWh)']}, "
        f"Weather Condition (Temp, °C): {row['Weather Condition (Temp, °C)']}, "
        f"Geographical Location: {row['Geographical Location']}, "
        f"Spike Detection: {row['Spike Detection']}, "
        f"Zero Consumption Periods: {row['Zero Consumption Periods']}, "
        f"Negative Readings: {row['Negative Readings']}, "
        f"Voltage (V): {row['Voltage (V)']}, "
        f"Current (A): {row['Current (A)']}, "
        f"Power Factor: {row['Power Factor']}, "
        f"Customer Type: {row['Customer Type']}, "
        f"Tamper Alert: {row['Tamper Alert']}, "
        f"Outlier Score: {row['Outlier Score']}, "
        f"Customer Profile: {row['Customer Profile']}, "
        f"Contractual Demand (kW): {row['Contractual Demand (kW)']}"
    )
    return inp
@login_required
def index(request):
    tampering_meter_ids = {
        'High Tampering': [],
        'Low Tampering': [],
        'Normal': []
    }
    
    estimated_time = None
    processed_filename = None

    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            processed_filename = f"processed_{csv_file.name}"
            file_path = os.path.join('uploads', processed_filename)
            
            # Save the uploaded file
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            df = pd.read_csv(file_path)
            num_rows = len(df)
            
            # Calculate estimated time (3 seconds per row)
            estimated_time = num_rows * 3  # in seconds

            keywords = ["Low Tampering", "High Tampering", "Normal"]
            labels = []
            root_causes = []

            for _, row in df.iterrows():
                inp = generate_inference_input(row)
                inputs = tokenizer([alpaca_prompt.format(inp, "")], return_tensors="pt").to("cuda")
                outputs = model.generate(**inputs, max_new_tokens=64, use_cache=True)
                decoded_output = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

                label = "Unknown"
                for keyword in keywords:
                    if keyword in decoded_output:
                        label = keyword
                        break

                if label in root_cause_mapping:
                    if label == "Normal":
                        root_cause = None
                    else:
                        root_cause = random.choice(root_cause_mapping[label])
                else:
                    root_cause = "Unknown"

                labels.append(label)
                root_causes.append(root_cause)
                
                # Append Meter IDs to respective tampering lists
                meter_id = row['Meter ID']
                if label in tampering_meter_ids:
                    tampering_meter_ids[label].append(str(meter_id))

                # Send email if tampering is detected
                email = row['E-mail']
                if label != "Normal":
                    send_mail(
                        subject="Tampering Alert",
                        message=f"Potential tampering detected on {row['Date']} for Meter ID {meter_id}.\nLabel: {label}\nRoot Cause: {root_cause}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )

            df['Label'] = labels
            df['Root Cause'] = root_causes

            # Save processed file
            processed_file_path = os.path.join('uploads', processed_filename)
            df.to_csv(processed_file_path, index=False)

            # Store the filename in the session
            request.session['processed_file'] = processed_filename

            return render(request, 'detection/index.html', {'tampering_meter_ids': tampering_meter_ids, 'processed_file_url': processed_filename, 'estimated_time': estimated_time})

    # Retrieve the filename from the session
    processed_filename = request.session.get('processed_file', None)
    return render(request, 'detection/index.html', {'tampering_meter_ids': tampering_meter_ids, 'estimated_time': estimated_time})

def calculate_processing_time(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)
        num_rows = len(df)
        # Calculate estimated time (3 seconds per row)
        estimated_time = num_rows * 3  # in seconds       
        return JsonResponse({'estimated_time': estimated_time})
    return JsonResponse({'error': 'No file uploaded or invalid request method.'}, status=400)

def download_file(request, filename):
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
    raise Http404

# # Store the path to the processed CSV file
# PROCESSED_FILE_PATH = 'uploads/processed_data.csv'

def search_meter_id(request):
    if request.method == 'GET':
        meter_id = request.GET.get('meter_id', '').strip()
        processed_filename = request.session.get('processed_file', None)

        if not processed_filename:
            return JsonResponse({'error': 'No processed file available'}, status=404)
        
        file_path = os.path.join('uploads', processed_filename)

        if meter_id:
            if not os.path.exists(file_path):
                return JsonResponse({'error': 'Processed CSV file not found'}, status=404)
                
            df = pd.read_csv(file_path)
            filtered_df = df[df['Meter ID'].astype(str) == meter_id]
            if not filtered_df.empty:
                result = filtered_df.to_dict(orient='records')
                return JsonResponse({'result': result})
            else:
                return JsonResponse({'error': 'No matching meter ID found'}, status=404)
        return JsonResponse({'error': 'Meter ID not provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'registration/login.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

def custom_logout(request):
    logout(request)
    return redirect('login')
