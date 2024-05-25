from twilio.rest import Client
import face_recognition
from PIL import Image, ImageDraw, ImageFont

font_size = 20
font = ImageFont.truetype("arial.ttf", font_size)

# Initialize Twilio client
account_sid = 'ACb830f8f3ee514f2e7360f562aba9843f'
auth_token = 'de6e952e3147cf76c31e1f27ba276abb'
twilio_phone_number = '+13345085407'
recipient_phone_number = '+917075340930'

client = Client(account_sid, auth_token)

# Send SMS function
def send_sms(message):
    client.messages.create(
        to=recipient_phone_number,
        from_=twilio_phone_number,
        body=message
    )

# Load known faces and their encodings
image_of_manju = face_recognition.load_image_file('./img/known/profile pic.jpeg')
manju_face_encoding = face_recognition.face_encodings(image_of_manju)[0]

image_of_steve = face_recognition.load_image_file('./img/known/profile pic.jpeg')
steve_face_encoding = face_recognition.face_encodings(image_of_steve)[0]

image_of_saikrishna = face_recognition.load_image_file('./img/known/profile pic.jpeg')
saikrishna_face_encoding = face_recognition.face_encodings(image_of_saikrishna)[0]

known_face_encodings = [
    manju_face_encoding,
    steve_face_encoding,
    saikrishna_face_encoding
]

known_face_names = [
    "Manju",
    "Dhana nivas",
    "Satwik"
]

# Define function to process a single image
def process_image(image_path):
    # Load test image
    test_image = face_recognition.load_image_file(image_path)

    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    # Convert to PIL format
    pil_image = Image.fromarray(test_image)
    draw = ImageDraw.Draw(pil_image)

    # Define the font size and color
    name_font_size = 45
    name_font_color = (255, 255, 255)  # White color

    # Load a font with the desired size
    name_font = ImageFont.truetype("arial.ttf", name_font_size)

    # Loop through faces in test image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown Person" if not any(matches) else known_face_names[matches.index(True)]
        print("Detected Name:", name)

        if name == "Unknown Person":
            send_sms("Unknown person detected!")
            # Draw a bracket around the face
            draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0), width=5)
            # Draw "Unknown" label inside the bracket
            text = "Unknown"
            draw.text((left + 6, bottom - 8), text, fill=name_font_color, font=name_font)
        else:
            send_sms(f"{name} detected!")
            # Draw box and label with increased font size and white color
            draw.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=5)
            draw.text((left + 6, bottom - 8), name, fill=name_font_color, font=name_font)

    del draw

    # Display image
    pil_image.show()

    # Save image
    pil_image.save('identify.jpg')

# List of image paths
test_image_paths = ['./img/groups/Manjunath.jpeg', './img/groups/Dhananivas.jpeg', './img/groups/Dillep.jpeg']

# Process each image
for image_path in test_image_paths:
    process_image(image_path)
    input("Press Enter to continue...")  # Wait for user to press Enter before proceeding to the next image






