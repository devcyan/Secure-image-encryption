from flask import Flask, render_template, request
import numpy as np
import cv2
import base64
import hashlib

app = Flask(__name__)

def convert_to_seed(key):
    """Convert alphanumeric key to numeric seed"""
    hash_obj = hashlib.sha256(key.encode())
    hash_hex = hash_obj.hexdigest()
    return int(hash_hex, 16) % (2**31 - 1)

def transform_colors(img, key):
    """Transform pixel colors using key-derived values"""
    seed = convert_to_seed(key)
    np.random.seed(seed)
    
    # Generate random transformation parameters
    r_transform = np.random.randint(0, 256, size=img.shape[:2])
    g_transform = np.random.randint(0, 256, size=img.shape[:2])
    b_transform = np.random.randint(0, 256, size=img.shape[:2])
    
    # Apply transformation to each channel
    r, g, b = cv2.split(img)
    r = (r.astype(np.uint16) + r_transform) % 256
    g = (g.astype(np.uint16) + g_transform) % 256
    b = (b.astype(np.uint16) + b_transform) % 256
    
    return cv2.merge((r.astype(np.uint8), g.astype(np.uint8), b.astype(np.uint8)))

def inverse_colors(img, key):
    """Reverse the color transformation"""
    seed = convert_to_seed(key)
    np.random.seed(seed)
    
    # Generate same transformation parameters
    r_transform = np.random.randint(0, 256, size=img.shape[:2])
    g_transform = np.random.randint(0, 256, size=img.shape[:2])
    b_transform = np.random.randint(0, 256, size=img.shape[:2])
    
    # Apply inverse transformation
    r, g, b = cv2.split(img)
    r = (r.astype(np.uint16) - r_transform + 256) % 256
    g = (g.astype(np.uint16) - g_transform + 256) % 256
    b = (b.astype(np.uint16) - b_transform + 256) % 256
    
    return cv2.merge((r.astype(np.uint8), g.astype(np.uint8), b.astype(np.uint8)))

def pixel_shuffle(img, key):
    seed = convert_to_seed(key)
    np.random.seed(seed)
    h, w, c = img.shape
    shuffled_img = np.zeros_like(img)
    
    for i in range(c):
        flat = img[:, :, i].flatten()
        idx = np.random.permutation(flat.shape[0])
        shuffled_img[:, :, i] = flat[idx].reshape(h, w)
        
    return shuffled_img

def pixel_unshuffle(img, key):
    seed = convert_to_seed(key)
    np.random.seed(seed)
    h, w, c = img.shape
    unshuffled_img = np.zeros_like(img)
    
    for i in range(c):
        flat = img[:, :, i].flatten()
        idx = np.random.permutation(flat.shape[0])
        inv_idx = np.zeros_like(idx)
        inv_idx[idx] = np.arange(flat.shape[0])
        unshuffled_img[:, :, i] = flat[inv_idx].reshape(h, w)
        
    return unshuffled_img

@app.route('/', methods=['GET', 'POST'])
def index():
    result_image = None
    if request.method == 'POST':
        img_file = request.files['image']
        key = request.form['key']
        action = request.form['action']

        # Read and process image in memory
        file_bytes = np.frombuffer(img_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if action == 'encrypt':
            # First: Transform colors
            result_img = transform_colors(img, key)
            # Second: Shuffle pixels
            result_img = pixel_shuffle(result_img, key)
        else:
            # First: Unshuffle pixels
            result_img = pixel_unshuffle(img, key)
            # Second: Reverse color transformation
            result_img = inverse_colors(result_img, key)

        # Convert to base64 for browser display
        _, buffer = cv2.imencode('.png', cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR))
        result_image = base64.b64encode(buffer).decode('utf-8')

    return render_template('index.html', result_image=result_image)

if __name__ == '__main__':
    app.run(debug=True)