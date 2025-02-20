import os
import shutil

from markdown import markdown_to_html_node

def main():
  is_public_exists = os.path.exists("public")
  if is_public_exists:
    shutil.rmtree("public")

  copy_files_from_folder_to_folder("static", "public")
  generate_pages_recursive("content", "template.html", "public")

def copy_files_from_folder_to_folder(from_folder, to_folder):
  print(f"Creating {to_folder}")
  os.mkdir(to_folder)
  list = os.listdir(from_folder)
  for item in list:
    is_file = os.path.isfile(os.path.join(from_folder, item))  
    if is_file:
      print(f"Copying {item} to {to_folder}")
      shutil.copy(os.path.join(from_folder, item), to_folder)
    else:
      from_folder_path = os.path.join(from_folder, item)
      to_folder_path = os.path.join(to_folder, item)
      copy_files_from_folder_to_folder(from_folder_path, to_folder_path)

def extract_title(markdown):
  lines = markdown.split("\n")
  for line in lines:
    if line.strip().startswith("# "):
      title = line.split("# ")[1].strip()
      return title

  raise Exception("Title not found")

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page form {from_path} using {template_path} to {dest_path}")

  dir_name = os.path.dirname(dest_path)
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)

  with open(from_path, "r") as file:
    markdown = file.read()
  
  with open(template_path, "r") as file:
    template = file.read()

  try:
    html_node = markdown_to_html_node(markdown)
  except Exception as e:
    print(f"Error: {e}")
    raise 

  title = extract_title(markdown) 

  html = template.replace("{{ Title }}", title)
  html = html.replace("{{ Content }}", html_node.to_html())

  with open(dest_path, "w") as file:
    file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  list = os.listdir(dir_path_content)
  for item in list:
    is_file = os.path.isfile(os.path.join(dir_path_content, item))  
    if is_file:
      if item.endswith(".md"):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        generate_page(from_path, template_path, dest_path)
    else:
      from_folder_path = os.path.join(dir_path_content, item)
      to_folder_path = os.path.join(dest_dir_path, item)
      generate_pages_recursive(from_folder_path, template_path, to_folder_path)

main()
