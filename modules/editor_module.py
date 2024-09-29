from moviepy.video.io.VideoFileClip import VideoFileClip 
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, ColorClip 
from moviepy.config import change_settings 


change_settings({"IMAGEMAGICK_BINARY": r"/usr/bin/convert"})

def cut_video(
    start_time,
    end_time,
    input_video="videos/video.mp4",
    output_video="videos/cut_video.mp4",
):
    video = VideoFileClip(input_video)
    cut_clip = video.subclip(start_time, end_time)
    cut_clip.write_videofile(output_video)


def create_vertical_video_with_text_and_image(
    video_path="videos/cut_video.mp4",
    output_path="videos/final_video.mp4",
    text="",
    image_path=None,
    font="'Times-New-Roman'",
):
    # Load video
    video = VideoFileClip(video_path)
    vertical_resolution = (1080, 1920)

    # Resize video to vertical format
    video_resized = video.resize(width=1080)
    if video_resized.h > 960:
        video_resized = video_resized.crop(y_center=video_resized.h // 2, height=960)
    else:
        video_resized = video_resized.set_position(("center", 400))

    # Create a solid white background clip
    white_background = ColorClip(size=vertical_resolution, color=(255, 255, 255))
    white_background = white_background.set_duration(video.duration)

    # Automatically adjust font size to fit within the box height
    max_box_height = 400
    fontsize = 50  # Start with an initial font size

    while True:
        # Create the text clip with the current font size
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color="black",
            size=(900, None),  # Width is fixed, height is automatic
            bg_color="white",
            font=font,
        ).set_duration(video.duration)

        # Check if the height of the generated text clip is within the allowed box height
        if txt_clip.h <= max_box_height:
            break
        fontsize -= 2  # Reduce font size if the text is too tall

    txt_clip_with_margin = txt_clip.set_position(("center", 1920 / 2 + 100))

    # Load and prepare image
    if image_path:
        image = ImageClip(image_path).resize(
            vertical_resolution
        )  # Resize image to fit the video
        image = image.set_duration(video.duration)
    else:
        image = None

    # Composite final video with the white background, video, text, and image
    clips_to_composite = [white_background, video_resized, txt_clip_with_margin]
    if image:
        clips_to_composite.append(image)

    video_with_text_and_image = CompositeVideoClip(
        clips_to_composite, size=vertical_resolution
    )

    # Write final video
    video_with_text_and_image.write_videofile(output_path, codec="libx264", fps=30)
