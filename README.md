# Secure-image-encryption

Secure Image Encryption is a web-based application built with Python and Flask that provides secure encryption and decryption for images. It utilizes a combination of pixel shuffling and color transformation based on a user-provided key. All processing is done in-memory, ensuring no images are stored on the server.

🚀 Features
📤 Upload images (JPG/PNG)

🔐 Encrypt and decrypt using text-based keys

🔁 Pixel shuffling and color transformation

🧠 SHA-256 based key hashing for randomness

🧊 Glassmorphism UI with responsive design

🖼️ View and download processed images instantly

🛠️ Tech Stack
Flask – Backend web framework

OpenCV – Image processing

NumPy – Efficient matrix operations

HTML + CSS (Glassmorphism) – Frontend

Base64 – In-memory image transfer

hashlib – Key hashing with SHA-256

📁 File Structure
graphql
Copy code
SecureImageEncryption/
│
├── app.py                  # Flask application with core encryption logic
├── Requirements.txt        # List of required Python packages
├── templates/
│   └── index.html          # Frontend HTML form and display
├── static/
│   └── styles.css          # Styling for the web interface (glassmorphism)
├── Secure_Image_Encryption_Project_Report.pdf  # Project documentation/report
📦 Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/SecureImageEncryption.git
cd SecureImageEncryption
Install dependencies:

bash
Copy code
pip install -r Requirements.txt
Run the Flask application:

bash
Copy code
python app.py
Open your browser and go to http://localhost:5000.

🧠 How It Works
Upload an image and enter a secret key.

The key is hashed using SHA-256 and used as a random seed.

For encryption:

Apply color transformation.

Shuffle pixels based on the key.

For decryption:

Unshuffle pixels.

Reverse the color transformation.

Download the processed image directly.

⚠️ Limitations
Supports JPG and PNG only

No preview of encrypted image before download

Large images may be memory intensive

💡 Future Improvements
Add support for more image formats (e.g., TIFF, WebP)

Add preview comparison of original vs encrypted

Implement client-side encryption using WebAssembly

Dark/Light mode toggle

