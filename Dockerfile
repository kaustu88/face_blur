FROM python:3.9

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY face_blur_simple.py /app/

RUN pip install flask opencv-python numpy

CMD ["python", "face_blur_simple.py"]
