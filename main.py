import cv2
import os
import shutil

def get_face_histogram_and_coords(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None, None  # No face detected
    
    x, y, w, h = faces[0]
    face_region = gray[y:y+h, x:x+w]
    
    # Calculate histogram of the face region
    hist = cv2.calcHist([face_region], [0], None, [256], [0,256])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    
    return hist, (x, y, w, h)

def compare_faces(hist1, hist2):
    # Same function as before
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR_ALT)

def moveToBlacklisted(name):
    sourcePath = "to_check/"+name+".jpg"
    destinationPath = "blacklisted/"+name+".jpg"
    if os.path.exists(destinationPath):
        print(f"{name} is already blacklisted")
        return

    shutil.copy(sourcePath,destinationPath)
    print(f"{name} has been Blacklisted!!!")

def save_user_image(name, image_path, dataset_folder):
    save_path = os.path.join(dataset_folder, f"{name}.jpg")
    if os.path.exists(save_path):
        print("The person is already in our database")
        return
    
    # Use shutil.move to handle the move across different drives or filesystems
    shutil.move(image_path, save_path)
    print(f"Image saved as {save_path}")

def load_blacklisted_faces(blacklisted_folder):
    blacklisted_faces = {}
    for filename in os.listdir(blacklisted_folder):
        hist, _ = get_face_histogram_and_coords(os.path.join(blacklisted_folder, filename))
        if hist is not None:
            blacklisted_faces[filename] = hist
    return blacklisted_faces

def check_against_blacklist(image_path, blacklisted_faces, threshold_value=0.5):
    hist, coords = get_face_histogram_and_coords(image_path)
    if hist is not None:
        for _, blacklisted_hist in blacklisted_faces.items():
            similarity = compare_faces(hist, blacklisted_hist)
            if similarity < threshold_value and coords is not None:
                print("Match found! Triggering alarm and calling 911...")
                trigger_alarm()
                call_911()
                return True
    return False

def trigger_alarm():
    print("ALARM! ALARM! ALARM!")

def call_911():
    print("Calling 911...")

def main():
    blacklisted_folder = 'blacklisted'
    dataset_folder = 'to_check'

    blacklisted_faces = load_blacklisted_faces(blacklisted_folder)
    
    print("Welcome to the Face Recognition Terminal App!")
    while True:
        print("1. Upload Images to Database")
        print("2. Scan Images By Name..")
        print("3. Suspicious Acitivity? Move to Blacklist")
        print("4. Exit")

        choice = input("Choose an option: ")
        
        if choice == '1':
            image_path = input("Please provide the path to the image: ")
            print("Uploading Images to the database....")
            if not os.path.exists(image_path):
                print("Image file not found!")
                continue
            
            name = input("Enter the name of the person: ")
            save_user_image(name, image_path, dataset_folder)
            

        elif choice == '2':
            name = input("Enter the name of the person: ")
            if check_against_blacklist(os.path.join(dataset_folder, f"{name}.jpg"), blacklisted_faces):
                continue
            
            print(f"{name} is not in the blacklist.")

        elif choice == '3':
            name = input("Please write the name of the person: ")
            moveToBlacklisted(name)
            continue

        
        elif choice == '3':
            print("Exiting the application.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
