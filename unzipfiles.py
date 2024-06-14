import os
import zipfile
import shutil

class UnzipFiles:
  def __init__(self, local_dir, target_dir):
    self.local_dir = local_dir
    self.target_dir = target_dir
    
  def unzip(self):
    
    extracted_dlls = []  # List to store extracted DLL filenames
    
    for filename in os.listdir(self.local_dir):
      if filename.endswith(".zip"):
        # Get full path for zip file
        filepath = os.path.join(self.local_dir, filename)

        # Extract DLL and get extracted DLL filename
        extracted_dll = self.extract_dll_from_zip(filepath)

        if extracted_dll:
          extracted_dlls.append(extracted_dll)
          print(f"Extracted DLL: {extracted_dll}\n")
          
          # Delete the extracted ZIP file after successful DLL extraction
          os.remove(filepath)
          
          # Move the extracted DLL to the target local_directory
          extracted_dll_basename = os.path.basename(extracted_dll)
          target_dll_path = os.path.join(self.target_dir, extracted_dll_basename)
          shutil.move(extracted_dll, target_dll_path)
          
          #Print each dll moved
          print(f"Moved DLL: {target_dll_path}")    
        
        else:
          print(f"No DLL found in {filename}")
          

    return extracted_dlls  # Return list of extracted DLL filenames

  def extract_dll_from_zip(self, filepath):
    if not os.path.exists(filepath):
      return None

    with zipfile.ZipFile(filepath, 'r') as zip_ref:
      files_list = zip_ref.namelist()
      for file in files_list:
        if file.endswith('.dll'):
          zip_ref.extract(file, self.local_dir)
          extracted_dll = os.path.join(os.path.dirname(filepath), file)
          return extracted_dll
    return None
            
            
            
# Example usage
data_local_dir = 'temp'
target_local_dir = str(os.getenv('LOCAL_DIR'))
unzipper = UnzipFiles(data_local_dir, target_local_dir)
extracted_dlls = unzipper.unzip()
print(f"Total extracted DLLs: {len(extracted_dlls)}")
