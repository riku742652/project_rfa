from google.cloud import vision


def call_vision_api(url):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = url

    try:
        response = client.text_detection(image=image)
        texts = response.text_annotations[0].description
        print('return message:\n{}'.format(texts))
    except Exception as e:
        print(e)
        return None

    return texts