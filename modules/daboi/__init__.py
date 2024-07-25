import random
from PIL import Image, ImageEnhance, ImageTransform
import numpy as np
from __main__ import hexo
import os 
import discord

def apply_bg_transparency(image_path, save_path,background_rgb=(137, 85, 255), tolerance=55):
    image = Image.open(image_path).convert('RGBA')
    
    background_color = np.array(background_rgb + (255,)) 
    image_np = np.array(image)
    diff = np.abs(image_np[:, :, :4] - background_color)
    mask = np.all(diff <= tolerance, axis=-1)
    image_np[mask] = [0, 0, 0, 0]
    transparent_image = Image.fromarray(image_np)
    
    transparent_image.save(save_path)

    print(f'Modified image saved as {save_path}')

def create_bg_transparency_gif(image_path,num_images=360):
    apply_bg_transparency(image_path,"result.png")
    image = Image.open("result.png")
    
    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    image_paths = []

    for i in range(num_images):
        x_offset = i / num_images
        image_path = os.path.join(temp_dir, f'image_{i:03d}.png')
        image.save(image_path)
        image_paths.append(image_path)

def apply_color_filter(image_path, save_path, filter_rgb,background_rgb=(137, 85, 255), tolerance=55, enhance_factor=1):
    
    image = Image.open(image_path).convert('RGBA')
    
    background_color = np.array(background_rgb + (255,)) 
    image_np = np.array(image)
    diff = np.abs(image_np[:, :, :4] - background_color)
    mask = np.all(diff <= tolerance, axis=-1)
    image_np[mask] = [0, 0, 0, 0]
    transparent_image = Image.fromarray(image_np)

    enhancer = ImageEnhance.Color(transparent_image)
    filtered_image = enhancer.enhance(enhance_factor)

    filtered_np = np.array(filtered_image)
    green_channel = filtered_np[:, :, 1]
    average_color = (filtered_np[:, :, 0] + green_channel + filtered_np[:, :, 2]) // 3


    filtered_np[:, :, 0] = filter_rgb[0]
    filtered_np[:, :, 1] = (filtered_np[:, :, 1]*0.5+filter_rgb[1])//1.5
    filtered_np[:, :, 2] = filter_rgb[2] 

    average_filtered_image = Image.fromarray(filtered_np)
    average_filtered_image.save(save_path)

    print(f'Modified image saved as {save_path}')

def apply_color_gradient_filter(image_path, save_path, filter_rgb1, filter_rgb2, background_rgb=(137, 85, 255), tolerance=55, enhance_factor=1,x_offset = 0):
    """
    Apply a gradient color filter to an image, making the specified background color transparent.
    Gradually transitions from filter_rgb1 to filter_rgb2.

    :param image_path: Path to the input image
    :param save_path: Path to save the modified image
    :param filter_rgb1: The first RGB color for the gradient (tuple, e.g., (255, 100, 0))
    :param filter_rgb2: The second RGB color for the gradient (tuple, e.g., (0, 255, 0))
    :param background_rgb: The RGB color to be made transparent (tuple, e.g., (137, 85, 255))
    :param tolerance: The tolerance level for color similarity (default is 55)
    :param enhance_factor: Factor to enhance the color intensity (default is 1)
    """
    # Load the image
    image = Image.open(image_path).convert('RGBA')

    # Convert background color to numpy array
    background_color = np.array(background_rgb + (255,)) 

    # Convert the image to a numpy array
    image_np = np.array(image)

    # Calculate the absolute difference between the image and the background color
    diff = np.abs(image_np[:, :, :4] - background_color)
    
    # Create a mask where the difference is less than the tolerance for all channels
    mask = np.all(diff <= tolerance, axis=-1)

    # Set the alpha channel to 0 for the background color and similar colors
    image_np[mask] = [0, 0, 0, 0]

    # Convert numpy array back to image
    transparent_image = Image.fromarray(image_np)

    # Apply a filter to the entire image (e.g., enhance color)
    enhancer = ImageEnhance.Color(transparent_image)
    filtered_image = enhancer.enhance(enhance_factor)

    # Convert the filtered image to numpy array for processing
    filtered_np = np.array(filtered_image)

    # Calculate gradient factor
    height, width = filtered_np.shape[:2]
    gradient = np.linspace(0, 1, width)
    
    # Apply offset to the gradient
    offset_gradient = (gradient + x_offset) % 1

    # Create the gradient filter
    gradient_filter = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(3):
        gradient_filter[:, :, i] = ((1 - offset_gradient) * filter_rgb1[i] + offset_gradient * filter_rgb2[i]).astype(np.uint8)

    # Apply the gradient filter to the image
    gradient_np = np.zeros_like(filtered_np)
    gradient_np[:, :, 0] = gradient_filter[:, :, 0]  # Red channel
    gradient_np[:, :, 1] = (filtered_np[:, :, 1]*0.5+gradient_filter[:,:,1])//1.5  # Green channel
    gradient_np[:, :, 2] = gradient_filter[:, :, 2]  # Blue channel
    gradient_np[:, :, 3] = filtered_np[:, :, 3]      # Alpha channel

    gradient_filtered_image = Image.fromarray(gradient_np)

    # Save the modified image
    gradient_filtered_image.save(save_path)

    print(f'Modified image saved as {save_path}')

def rotate_image(image_path, save_path, degrees):
    
    with Image.open(image_path) as img:
        rotated_img = img.rotate(degrees, expand=True)
        rotated_img.save(save_path)

    print(f'Rotated image saved as {save_path}')

def rotate_image_x(image_path, save_path, angle):

    with Image.open(image_path) as img:
        # Convert angle to radians
        angle_rad = np.deg2rad(angle)
        
        # Calculate skew factors
        skew_factor = np.tan(angle_rad / 2)
        
        # Define a transformation matrix for skewing
        matrix = (1, skew_factor, 0,
                  0, 1, 0,
                  0, 0, 1)
        
        # Apply the skew transformation
        width, height = img.size
        transformed_img = img.transform((width, height), Image.AFFINE, matrix)
        
        # Save the skewed image
        transformed_img.save(save_path)

    print(f'Skewed image (X axis simulation) saved as {save_path}')

def create_gif_from_images(image_paths, gif_path, duration=360,background_rgb=(137, 85, 255)):
    """
    Compile multiple images into a GIF.

    :param image_paths: List of paths to images to include in the GIF
    :param gif_path: Path to save the resulting GIF
    :param duration: Duration of each frame in the GIF (milliseconds)
    """
    images = []
    
    for path in image_paths:
        img = Image.open(path)
        background = Image.new('RGBA', img.size, background_rgb + (255,))
        
        # Composite the original image onto the background
        combined = Image.alpha_composite(background, img)
        images.append(combined)
        
    
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )

    print(f'GIF saved as {gif_path}')

def apply_gradient_gif(base_image_path, output_gif_path, filter_rgb1, filter_rgb2, num_images=360):
    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    image_paths = []

    for i in range(num_images):
        x_offset = i / 25
        image_path = os.path.join(temp_dir, f'image_{i:03d}.png')
        apply_color_gradient_filter(
            image_path,
            image_path,
            filter_rgb1,
            filter_rgb2,
            x_offset=x_offset
        )
        image_paths.append(image_path)

def apply_transition_gif(base_image_path, output_gif_path, filter_rgb1, filter_rgb2, num_images=360):
    """
    Generate a series of images transitioning from one color filter to another and compile them into a GIF.

    :param base_image_path: Path to the base image
    :param output_gif_path: Path to save the resulting GIF
    :param filter_rgb1: The first RGB color for the transition (tuple, e.g., (255, 100, 0))
    :param filter_rgb2: The second RGB color for the transition (tuple, e.g., (0, 255, 0))
    :param num_images: Number of images to generate
    """
    # Directory to save temporary images
    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    image_paths = []

    for i in range(num_images):
        # Calculate blend factor
        factor = i / (num_images - 1)
        filter_rgb = (
            int((1 - factor) * filter_rgb1[0] + factor * filter_rgb2[0]),
            int((1 - factor) * filter_rgb1[1] + factor * filter_rgb2[1]),
            int((1 - factor) * filter_rgb1[2] + factor * filter_rgb2[2])
        )
        
        image_path = os.path.join(temp_dir, f'image_{i:03d}.png')
        apply_color_filter(
            image_path,
            image_path,
            filter_rgb
        )
        image_paths.append(image_path)

def apply_rotation_gif(base_image_path, output_gif_path,num_images=360):
    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    image_paths = []

    for i in range(num_images):
        rotation = i
        image_path = os.path.join(temp_dir, f'image_{i:03d}.png')
        rotate_image(
            image_path,
            image_path,
            rotation
        )
        image_paths.append(image_path)

def apply_rotation_x_gif(base_image_path, output_gif_path,num_images=360):
    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    image_paths = []

    for i in range(num_images):
        rotation = i
        image_path = os.path.join(temp_dir, f'image_{i:03d}.png')
        rotate_image_x(
            image_path,
            image_path,
            rotation
        )
        image_paths.append(image_path)


def change_gif_fps(input_gif_path, output_gif_path, fps):
    """
    Change the FPS of a GIF by adjusting the duration of each frame.

    :param input_gif_path: Path to the input GIF
    :param output_gif_path: Path to save the modified GIF
    :param fps: Desired frames per second
    """
    # Calculate the duration for each frame in milliseconds
    duration_ms = int(1000 / fps)

    # Open the GIF
    with Image.open(input_gif_path) as img:
        # Collect all frames
        frames = []
        try:
            while True:
                # Append the frame with the new duration
                frame = img.copy()
                frames.append(frame)
                img.seek(img.tell() + 1)
        except EOFError:
            pass

        # Save the GIF with the new FPS
        frames[0].save(
            output_gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0
        )

    print(f'GIF with changed FPS saved as {output_gif_path}')

def generate_random_boi():
    
    background_rgb=(137, 85, 255)
    temp_dir = 'temp_images'
            
    data = {
        "color1":(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
        "color2":(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
        "angle1":random.randint(1,360),
        "angle2":random.randint(1,360),
        "gradient":random.randint(1,10) == 1,
        "gradient_offset":random.randint(0,100)/100,
        "gradient_animated":random.randint(1,100) == 1,
        "transition_animated":random.randint(1,100) == 1,
        "rotate":random.randint(1,25) == 1,
        "rotate_x":random.randint(1,50) == 1,
        "animate_rotate": random.randint(1,100) == 1,
    }
    
    data["animated"] = data["gradient_animated"] or data["transition_animated"] or data["animate_rotate"] 
    
    if data["animated"]:
        
        create_bg_transparency_gif(os.path.dirname(__file__)+"/base.webp")
        
        if data["gradient_animated"]:
            apply_gradient_gif("a","a",data["color1"],data["color2"])
            
        if data["transition_animated"]:
            apply_transition_gif("a","a",data["color1"],data["color2"])
            
            
        if data["animate_rotate"]:
            apply_rotation_gif("a","a")
            
        for i in range(360):
            image_path = os.path.join(temp_dir, f'image_{i:03d}.png')
            if not data["gradient"]:
                apply_color_filter(image_path,image_path,data["color1"])
            else:
                apply_color_gradient_filter(image_path,image_path,data["color1"],data["color2"],x_offset=data["gradient_offset"])
                
            if data["rotate"]:
                rotate_image(image_path,image_path,data["angle1"])
                 
        
        image_paths = []

        for i in range(360):
            image_path = os.path.join(temp_dir, f'image_{i:03d}.png')
            image_paths.append(image_path)

        create_gif_from_images(image_paths, "result.gif")

        #for path in image_paths:
            #os.remove(path)
        #os.rmdir(temp_dir)
        
        change_gif_fps("result.gif","result.gif",360)
        
    else:
        apply_bg_transparency(os.path.dirname(__file__)+"/base.webp", 'result.png')

        if not data["gradient"]:
            apply_color_filter("result.png","result.png",data["color1"])
        else:
            apply_color_gradient_filter("result.png","result.png",data["color1"],data["color2"],x_offset=data["gradient_offset"])
            
        if data["rotate"]:
            rotate_image("result.png","result.png",data["angle1"])
        
    
        img = Image.open("result.png")
    
        background = Image.new('RGBA', img.size, background_rgb + (255,))
        combined = Image.alpha_composite(background, img)
        
        combined.save("result.png")
    
    return data

@hexo.client.tree.command(name="boi")
async def react_rules(ctx):

    
    embed=discord.Embed(title="Loading...", description="Please wait while we open your boi. ", color=0x58b9ff)

    await ctx.response.send_message(embed=embed,ephemeral=True)
    
    data = generate_random_boi()
    
    if data["animated"] :
        embed=discord.Embed(title=f"{ctx.user.display_name}'s Boi", description="The item has been added to your </farm:1146549817959522354>", color=0x58b9ff)
        file = discord.File("result.gif", filename="result.gif")
        embed.set_image(url="attachment://result.gif")
        await ctx.channel.send(embed=embed,file=file)   
    else:
        embed=discord.Embed(title=f"{ctx.user.display_name}'s Boi", description="The item has been added to your </farm:1146549817959522354>", color=0x58b9ff)
        file = discord.File("result.png", filename="result.png")
        embed.set_image(url="attachment://result.png")
        await ctx.channel.send(embed=embed,file=file)
    
functions = {}