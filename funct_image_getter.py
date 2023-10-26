import simple_image_download.simple_image_download as simp
import re
import requests
from PIL import Image, ImageFont, ImageDraw

filepath = ""
with open("filepath.txt") as file:
    for line in file.readlines():
        filepath = line

my_downloader = simp.Downloader()
my_downloader.extensions = '.jpg'

def write_source(img_path, caption):
    I=Image.open(filepath + img_path)

    Im = ImageDraw.Draw(I)

    x = 0
    y = 0
    charsperline = 60

    tempinput = ""
    paragraph = caption
    for i, letter in enumerate(paragraph):
        if i % charsperline == 0:
            Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

            Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))
            tempinput = ""
            y += 15
        tempinput += letter

    Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
    Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
    Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
    Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

    Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))

    I.save(filepath + img_path)



def download_images(keywords, num, index, paragraph):
    keywords = keywords.replace(" ", "d328749201d")
    keywords = re.sub('[\W_]+', '', keywords)
    keywords = keywords.replace("d328749201d", "+")
    print("searching.. ", keywords)
    try:
        my_downloader.search_urls(keywords,limit=8, verbose=False)
        url_list = my_downloader.get_urls()
    except Exception:
        url_list = []

    if len(url_list) == 0 or keywords == "noimagefound":
        for i in range(0, num):
            img_data = requests.get('https://i.ibb.co/SyF2DWV/No-Image-Available.jpg').content
            with open(filepath + 'image_folder/' + str(index) + str(i) + '.jpg', 'wb') as handler:
                handler.write(img_data)

            image_path = filepath + 'image_folder/' + str(index) + str(i) + '.jpg'
            source = 'https://i.ibb.co/SyF2DWV/No-Image-Available.jpg'
            image = Image.open(image_path).resize((400, 400), Image.ANTIALIAS)
            image.save(image_path)

            I=Image.open(image_path)

            Im = ImageDraw.Draw(I)
            
            x = 20
            y = 100
            charsperline = 60

            tempinput = ""
            for i, letter in enumerate(paragraph):
                if i % charsperline == 0:
                    Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                    Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                    Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                    Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

                    Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))
                    tempinput = ""
                    y += 15
                tempinput += letter

            Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

            Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))



            

            I.save(image_path)

            write_source(image_path, source)
            
    else:
        ind = 0
        source = ""
        for i in range(0, num):
            if i >= len(url_list):
                img_data = requests.get('https://i.ibb.co/SyF2DWV/No-Image-Available.jpg').content 
                source = 'https://i.ibb.co/SyF2DWV/No-Image-Available.jpg' 
            else:
                try:
                    img_data = requests.get(url_list[i]).content
                    source = url_list[i]
                except Exception:
                    img_data = requests.get('https://i.ibb.co/SyF2DWV/No-Image-Available.jpg').content  
                    source = 'https://i.ibb.co/SyF2DWV/No-Image-Available.jpg'
            try:
                with open(filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + '.jpg', 'wb') as handler:
                    handler.write(img_data)
                

                image_path = filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + '.jpg'
                image = Image.open(image_path).resize((400, 400), Image.ANTIALIAS)
                image.save(image_path)

                I=Image.open(image_path)

                Im = ImageDraw.Draw(I)
                
                x = 20
                y = 100
                charsperline = 60

                tempinput = ""
                for i, letter in enumerate(paragraph):
                    if i % charsperline == 0:
                        Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                        Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                        Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                        Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

                        Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))
                        tempinput = ""
                        y += 15
                    tempinput += letter

                Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

                Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))



                

                I.save(image_path)

                write_source(image_path, source)


            except Exception:
                with open(filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + '.jpg', 'wb') as handler:
                    img_data = requests.get('https://i.ibb.co/SyF2DWV/No-Image-Available.jpg').content  
                    handler.write(img_data)
                    source = 'https://i.ibb.co/SyF2DWV/No-Image-Available.jpg'
                
                image_path = filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + '.jpg'
                image = Image.open(image_path).resize((400, 400), Image.ANTIALIAS)
                image.save(image_path)

                I=Image.open(image_path)

                Im = ImageDraw.Draw(I)
                
                x = 20
                y = 100
                charsperline = 60

                tempinput = ""
                for i, letter in enumerate(paragraph):
                    if i % charsperline == 0:
                        Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                        Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                        Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                        Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

                        Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))
                        tempinput = ""
                        y += 15
                    tempinput += letter

                Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
                Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

                Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))



                

                I.save(image_path)

                write_source(image_path, source)
                
            ind += 1

    my_downloader.flush_cache()



    return 1

'''
# Change Direcotory
my_downloader.directory = 'my_dir/'
# Change File extension type
my_downloader.extensions = '.jpg'
print(my_downloader.extensions)
my_downloader.download('laptop', limit=10, verbose=True)
'''