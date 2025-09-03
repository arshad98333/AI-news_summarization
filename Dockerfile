# Use the official Hugging Face base image for Gradio Spaces
FROM hf-base

# [CRITICAL STEP]
# Tell the operating system to install chromium and its dependencies.
# This command is more robust than using packages.txt.
RUN apt-get update && apt-get install -y chromium libgl1

# Copy all your project files (main.py, requirements.txt, etc.) into the container
COPY . .

# Install all your Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Tell the container what command to run when it starts.
# This runs your Gradio app.
CMD ["python", "main.py"]