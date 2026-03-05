from django.shortcuts import render

# Create your views here.
import subprocess
import threading
from django.shortcuts import render, redirect
from .models import MigrationTask

def dashboard(request):
    tasks = MigrationTask.objects.all().order_by('-created_at')[:10]
    return render(request, 'migrator/dashboard.html', {'tasks': tasks})

def run_migration(request):
    if request.method == "POST":
        src_email = request.POST.get('src_email')
        src_pass = request.POST.get('src_pass')
        dest_email = request.POST.get('dest_email')
        dest_pass = request.POST.get('dest_pass')
        folder = request.POST.get('folder')
        is_dry_run = request.POST.get('dry_run') == 'on'

        # Create the DB entry
        task = MigrationTask.objects.create(
            source_email=src_email,
            destination_email=dest_email,
            folder_name=folder,
            status="Running"
        )

        # Build the command
        cmd = [
            "imapsync", "--host1", "imappro.zoho.com", "--user1", src_email, "--pass1", src_pass,
            "--host2", "imappro.zoho.com", "--user2", dest_email, "--pass2", dest_pass,
            "--ssl1", "--ssl2", "--subfolder2", folder, "--syncinternaldates", "--automap"
        ]
        if is_dry_run:
            cmd.append("--dry")

        # Run in background thread so the web page doesn't hang
        thread = threading.Thread(target=execute_imapsync, args=(task.id, cmd))
        thread.start()

        return redirect('dashboard')

def execute_imapsync(task_id, cmd):
    task = MigrationTask.objects.get(id=task_id)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in iter(process.stdout.readline, ""):
        task.log_output += line
        task.save() # Real-time logging to DB
        
    process.stdout.close()
    task.status = "Completed"
    task.save()