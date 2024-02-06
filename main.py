import requests, os, sys, pygame
from PIL import Image
from io import BytesIO

pygame.init()
size = width, height = 400, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, *groups):
        super().__init__(all_sprites, *groups)
        self.image = pygame.Surface((rect[2], rect[3]),
                                    pygame.SRCALPHA, 32)
        self.rect = rect
        pygame.draw.rect(self.image, (255, 255, 255), self.rect, 3)
        font = pygame.font.Font(None, 12)
        text = font.render(text, True, (255, 255, 255))
        self.image.blit(text, (0, 0))
        self.mask = self.rect

def refresh(lo, la, scale):
    params = {
        "ll": ",".join([lo, la]),
        "spn": ",".join([scale, scale]),
        "l": "map",
        "size": "400,400",
        "l": layers[current_layer]
    }
    response = requests.get(api_server, params=params)
    img1 = Image.open(BytesIO(
        response.content))
    img1.save("data/map.png")
    img = load_image("map.png")
    screen.fill((0, 0, 0))
    screen.blit(img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


api_server = "http://static-maps.yandex.ru/1.x/"

lon = "37.530887"
lat = "55.703118"
delta = "0.002"
layers = ["map", "sat", "skl"]
current_layer = 0

params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "map",
    "size": "400,400"
}
response = requests.get(api_server, params=params)
img1 = Image.open(BytesIO(
    response.content))
img1.save("data/map.png")
img = load_image("map.png")
screen.fill((0, 0, 0))
screen.blit(img, (0, 0))
view_button = pygame.sprite.Group()
Button((0, 400, 200, 100), "View", view_button)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if float(delta) > 0.0001:
                    delta = str(float(delta) / 1.2)
                    refresh(lon, lat, delta)
                else:
                    delta = "0.001"
            elif event.key == pygame.K_PAGEUP:
                if float(delta) < 90:
                    delta = str(float(delta) * 1.2)
                    refresh(lon, lat, delta)
                else:
                    delta = "90"
            elif event.key == pygame.K_UP:
                lat = str((float(lat) + (float(delta) / 2)) % 90)
                refresh(lon, lat, delta)
            elif event.key == pygame.K_DOWN:
                lat = str((float(lat) - (float(delta) / 2)) % 90)
                refresh(lon, lat, delta)
            elif event.key == pygame.K_LEFT:
                lon = str((float(lon) - (float(delta) / 2)) % 180)
                refresh(lon, lat, delta)
            elif event.key == pygame.K_RIGHT:
                lon = str((float(lon) + (float(delta) / 2)) % 180)
                refresh(lon, lat, delta)
            elif event.key == pygame.K_l:
                current_layer += 1
                current_layer %= 3
                refresh(lon, lat, delta)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
