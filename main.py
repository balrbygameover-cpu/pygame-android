import pygame
import sys
import arabic_reshaper
from bidi.algorithm import get_display

# تشغيل بايثون
pygame.init()

# إعدادات الشاشة
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("صانع الألعاب المصري - Roblox Ultimate: Worm Maps, Brainrot Lasers & All Tools")

# الألوان
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
BLUE = (0, 130, 255)
GREEN = (0, 210, 110)
RED = (255, 60, 60)
PURPLE = (160, 32, 240)
SPAWN_COLOR = (245, 245, 255)
VAULT_COLOR = (140, 140, 150)
LASER_COLOR = (255, 0, 80)
WORM_COLOR = (50, 205, 50)  # لون دودة الماب الأخضر
CARD_BG = (35, 45, 65)

# أنواع المشايات وسرعاتها المضاعفة
CONVEYOR_TYPES = [
    {"name": "مشاية خشبية (سرعة ×2)", "multiplier": 2, "color": (160, 100, 40)},
    {"name": "مشاية حديد (سرعة ×4)", "multiplier": 4, "color": (120, 130, 145)},
    {"name": "مشاية دهب (سرعة ×12)", "multiplier": 12, "color": (255, 215, 0)},
    {"name": "مشاية ألماس (سرعة ×14)", "multiplier": 14, "color": (0, 220, 255)},
    {"name": "المشاية الحمراء الأسطورية (سرعة ×150)", "multiplier": 150, "color": (255, 30, 50)}
]
current_conveyor_index = 0

COLORS = [
    ("كيبورد أسود فاخر", (45, 45, 55)),
    ("أخضر إضاءة", (0, 210, 110)),
    ("أزرق نيون", (0, 130, 255)),
    ("أصفر تكتيكي", (255, 200, 0)),
    ("بنفسجي سحري", (160, 32, 240)),
    ("رمادي ستيل", (100, 110, 125))
]
current_color_index = 0

# قاعدة بيانات المابات (مابات كتيرة جاهزة: بيت، سرقة، دود، وباركور)
PUBLISHED_MAPS = [
    {
        "name": "1. ماب الدود المرعب وبرين روت", 
        "creator": "عبدالعزيز", 
        "spawn": [80, 380],
        "blocks": [
            (pygame.Rect(50, 450, 820, 35), (45, 45, 55))
        ], 
        "conveyors": [
            {"rect": pygame.Rect(250, 425, 100, 25), "multiplier": 150, "color": (255, 30, 50), "name": "المشاية الحمراء"}
        ],
        "lasers": [
            {"rect": pygame.Rect(450, 350, 15, 100), "name": "حاجز برين روت"}
        ],
        "worms": [
            {"rect": pygame.Rect(600, 410, 90, 40), "speed": 4.0, "name": "الدودة العملاقة"}
        ],
        "vaults": [pygame.Rect(750, 390, 50, 60)],
        "color": (50, 205, 50)
    },
    {
        "name": "2. ماب البنك والسرقة الكبرى", 
        "creator": "أحمد", 
        "spawn": [100, 380],
        "blocks": [
            (pygame.Rect(50, 450, 820, 35), (100, 110, 125))
        ],
        "conveyors": [],
        "lasers": [],
        "worms": [],
        "vaults": [pygame.Rect(650, 390, 50, 60), "vault2"],
        "color": (255, 215, 0)
    }
]
FRIENDS_LIST = ["أحمد (أونلاين)", "يوسف (في لعبة)", "محمود (غير متصل)"]

font = pygame.font.SysFont("arial", 20)
font_large = pygame.font.SysFont("arial", 26)

def draw_arabic_text(text, font_obj, color, surface, x, y):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    textobj = font_obj.render(bidi_text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill((20, 24, 33))
        draw_arabic_text("صانع مابات Roblox الشاملة (دود، بيت، سرقة، برين روت)", font_large, WHITE, screen, 150, 40)
        
        pygame.draw.rect(screen, BLUE, (325, 130, 250, 45), border_radius=10)
        pygame.draw.rect(screen, GREEN, (325, 185, 250, 45), border_radius=10)
        pygame.draw.rect(screen, PURPLE, (325, 240, 250, 45), border_radius=10)
        pygame.draw.rect(screen, (220, 110, 0), (325, 295, 250, 45), border_radius=10)
        pygame.draw.rect(screen, (0, 200, 200), (325, 350, 250, 45), border_radius=10)
        
        draw_arabic_text("تصفح مابات المجتمع الكثيرة", font, WHITE, screen, 350, 140)
        draw_arabic_text("اصنع ماب جديد (دود، سرقة، بيت)", font, WHITE, screen, 330, 195)
        draw_arabic_text("قائمة الأصدقاء", font, WHITE, screen, 395, 250)
        draw_arabic_text("معرض جميع أدوات روبلوكس", font, WHITE, screen, 350, 305)
        draw_arabic_text("نشر اللعبة رسمياً أونلاين", font, BLACK, screen, 355, 360)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 325 <= mouse_pos[0] <= 575:
                    if 130 <= mouse_pos[1] <= 175:
                        play_community_maps()
                    elif 185 <= mouse_pos[1] <= 230:
                        create_mode()
                    elif 240 <= mouse_pos[1] <= 285:
                        friends_menu()
                    elif 295 <= mouse_pos[1] <= 340:
                        monsters_menu()
                    elif 350 <= mouse_pos[1] <= 395:
                        publish_game_online()
        pygame.display.update()

def publish_game_online():
    running = True
    while running:
        screen.fill((20, 24, 33))
        draw_arabic_text("منصة نشر اللعبة رسمياً لجميع اللاعبين:", font_large, WHITE, screen, 240, 40)
        
        pygame.draw.rect(screen, CARD_BG, (150, 120, 600, 150), border_radius=12)
        draw_arabic_text("مبروك يا عبدالعزيز! اللعبة جاهزة للنشر برقم إصدار Roblox Ultimate v3.0", font, GREEN, screen, 180, 145)
        draw_arabic_text("• عدد المابات الجاهزة: متوفر مابات دود، سرقة وبنوك، وبيوت", font, WHITE, screen, 180, 190)
        draw_arabic_text("• الحالة: جاهزة للرفع على سيرفرات ألعاب الكوميونيتي!", font, WHITE, screen, 180, 230)
        
        pygame.draw.rect(screen, BLUE, (350, 330, 200, 50), border_radius=10)
        draw_arabic_text("تأكيد النشر للجمهور", font, WHITE, screen, 370, 342)
        
        draw_arabic_text("دوس ESC للرجوع للقائمة", font, (180, 180, 180), screen, 380, 450)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 350 <= event.pos[0] <= 550 and 330 <= event.pos[1] <= 380:
                    notice_timer = 120
                    return
        pygame.display.update()

def friends_menu():
    running = True
    while running:
        screen.fill((20, 24, 33))
        draw_arabic_text("قائمة الأصدقاء المتصلين:", font_large, WHITE, screen, 330, 50)
        y_offset = 150
        for friend in FRIENDS_LIST:
            pygame.draw.rect(screen, CARD_BG, (250, y_offset, 400, 45), border_radius=8)
            draw_arabic_text(f"• {friend}", font, (0, 255, 120), screen, 270, y_offset + 10)
            y_offset += 60
        draw_arabic_text("دوس ESC للرجوع", font, (180, 180, 180), screen, 380, 550)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        pygame.display.update()

def monsters_menu():
    running = True
    while running:
        screen.fill((20, 24, 33))
        draw_arabic_text("معرض أدوات روبلوكس الشاملة لإنشاء مابات لا حصر لها:", font_large, WHITE, screen, 180, 25)
        
        tools_info = [
            ("أدوات ماب الدود (Worm Maps):", "دودة عملاقة مرعبة تطاردك وتتحرك في الماب لتدمير اللاعبين."),
            ("أدوات حواجز برين روت (Brainrot Lasers):", "أمن الليزر القاتل الذي يكشف الحرامية ويقضي عليهم فوراً."),
            ("أدوات ماب السرقة والبنك:", "خزائن أموال كبرى وسرقة الملايين وتجميع الكاش."),
            ("أدوات ماب البيت والديزاين:", "جدران، غرف، وأثاث لتصميم منزل الأحلام والفلل."),
            ("مشايات السرعة الخارقة:", "5 أنواع مشايات (خشب، حديد، دهب، ألماس، حمراء ×150).")
        ]
        
        y_pos = 85
        for title, desc in tools_info:
            pygame.draw.rect(screen, CARD_BG, (120, y_pos, 660, 55), border_radius=8)
            draw_arabic_text(f"• {title}", font, GREEN, screen, 140, y_pos + 8)
            draw_arabic_text(desc, font, WHITE, screen, 160, y_pos + 30)
            y_pos += 65

        draw_arabic_text("دوس ESC للرجوع", font, (180, 180, 180), screen, 380, 590)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        pygame.display.update()

def play_community_maps():
    running = True
    notice_timer = 0
    notice_text = ""
    
    while running:
        screen.fill((20, 24, 33))
        draw_arabic_text("اختر ماب من مابات المجتمع الكثيرة للعب:", font_large, WHITE, screen, 250, 25)
        
        card_data = []
        y_pos = 85
        for i, m in enumerate(PUBLISHED_MAPS):
            c_rect = pygame.Rect(100, y_pos, 520, 90)
            play_btn = pygame.Rect(630, y_pos + 20, 85, 48)
            delete_btn = pygame.Rect(725, y_pos + 20, 85, 48)
            
            card_data.append((c_rect, play_btn, delete_btn, m))
            
            pygame.draw.rect(screen, CARD_BG, c_rect, border_radius=12)
            thumb_rect = pygame.Rect(115, y_pos + 10, 70, 70)
            pygame.draw.rect(screen, m['color'], thumb_rect, border_radius=8)
            
            draw_arabic_text(m['name'], font, WHITE, screen, 195, y_pos + 12)
            draw_arabic_text(f"المطور: {m['creator']} | دود، سرقة، وليزر برين روت", font, (160, 175, 192), screen, 195, y_pos + 45)
            
            pygame.draw.rect(screen, GREEN, play_btn, border_radius=8)
            draw_arabic_text("العب", font, BLACK, screen, 655, y_pos + 30)
            
            pygame.draw.rect(screen, RED, delete_btn, border_radius=8)
            draw_arabic_text("مسح", font, WHITE, screen, 750, y_pos + 30)
            
            y_pos += 105
            
        if notice_timer > 0:
            draw_arabic_text(notice_text, font, RED, screen, 280, 580)
            notice_timer -= 1
            
        draw_arabic_text("دوس ESC للرجوع للقائمة الرئيسية", font, WHITE, screen, 340, 615)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for c_rect, play_btn, delete_btn, m in card_data:
                    if play_btn.collidepoint(event.pos):
                        run_game_map(m)
                    elif delete_btn.collidepoint(event.pos):
                        if m['creator'] == "عبدالعزيز":
                            PUBLISHED_MAPS.remove(m)
                            notice_text = "تم مسح الماب بنجاح يا عبدالعزيز!"
                            notice_timer = 120
                            break
                        else:
                            notice_text = "خطأ: لا يمكنك مسح ماب لم تقم بإنشائه!"
                            notice_timer = 120
                            break
                            
        pygame.display.update()

def draw_roblox_character(surface, x, y, shirt_color=BLUE):
    pygame.draw.rect(surface, (255, 215, 170), (x + 6, y, 18, 18), border_radius=4)
    pygame.draw.rect(surface, (40, 40, 50), (x + 8, y + 4, 14, 5), border_radius=2)
    pygame.draw.rect(surface, shirt_color, (x + 3, y + 18, 24, 26), border_radius=5)
    pygame.draw.rect(surface, (255, 215, 170), (x - 3, y + 18, 5, 22), border_radius=2)
    pygame.draw.rect(surface, (255, 215, 170), (x + 28, y + 18, 5, 22), border_radius=2)
    pygame.draw.rect(surface, (30, 30, 40), (x + 4, y + 44, 9, 16), border_radius=3)
    pygame.draw.rect(surface, (30, 30, 40), (x + 17, y + 44, 9, 16), border_radius=3)

def run_game_map(map_data):
    spawn_x, spawn_y = map_data.get('spawn', [100, 100])
    p_x, p_y = spawn_x, spawn_y
    p_vy = 0
    gravity = 0.5
    base_speed = 4.0
    score_cash = 0
    deaths_count = 0
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill((30, 35, 48))
        draw_arabic_text(f"الماب: {map_data['name']}", font, WHITE, screen, 20, 15)
        draw_arabic_text(f"فلوس السرقة: {score_cash} | مرات الموت: {deaths_count}", font, (0, 240, 255), screen, 20, 45)
        
        # نقطة الريسبون البيضاء
        spawn_rect = pygame.Rect(spawn_x, spawn_y + 20, 40, 40)
        pygame.draw.rect(screen, SPAWN_COLOR, spawn_rect, border_radius=8)
        draw_arabic_text("SPAWN", font, BLACK, screen, spawn_rect.x + 2, spawn_rect.y + 8)
        
        p_vy += gravity
        p_y += p_vy
        player_rect = pygame.Rect(p_x, p_y, 30, 60)
        
        if p_y > SCREEN_HEIGHT + 50:
            p_x, p_y = spawn_x, spawn_y
            p_vy = 0
            deaths_count += 1

        on_ground = False
        for block, color in map_data['blocks']:
            pygame.draw.rect(screen, color, block, border_radius=4)
            if player_rect.colliderect(block) and p_vy > 0:
                p_y = block.y - 60
                p_vy = 0
                on_ground = True
                
        # مشايات السرعة
        current_speed = base_speed
        for conv in map_data.get('conveyors', []):
            pygame.draw.rect(screen, conv['color'], conv['rect'], border_radius=6)
            if player_rect.colliderect(conv['rect']):
                current_speed = base_speed * conv['multiplier']
                p_x += 2

        # حواجز برين روت (ليزر أمني قاتل)
        for laser in map_data.get('lasers', []):
            pygame.draw.rect(screen, LASER_COLOR, laser['rect'], border_radius=3)
            pygame.draw.rect(screen, WHITE, (laser['rect'].x + 3, laser['rect'].y, 3, laser['rect'].height))
            if player_rect.colliderect(laser['rect']):
                p_x, p_y = spawn_x, spawn_y
                p_vy = 0
                deaths_count += 1

        # دودة الماب المرعبة (Worm)
        for worm in map_data.get('worms', []):
            w_rect = worm['rect']
            if w_rect.x < p_x: w_rect.x += worm.get('speed', 3)
            elif w_rect.x > p_x: w_rect.x -= worm.get('speed', 3)
            
            pygame.draw.rect(screen, WORM_COLOR, w_rect, border_radius=15)
            pygame.draw.circle(screen, BLACK, (w_rect.x + 15, w_rect.y + 10), 5)
            pygame.draw.circle(screen, BLACK, (w_rect.x + 45, w_rect.y + 10), 5)
            draw_arabic_text("دودة الماب", font, WHITE, screen, w_rect.x, w_rect.y - 22)

            if player_rect.colliderect(w_rect):
                p_x, p_y = spawn_x, spawn_y
                p_vy = 0
                deaths_count += 1

        # خزائن الأموال (ماب السرقة)
        for vault in map_data.get('vaults', []):
            if isinstance(vault, pygame.Rect):
                v_rect = vault
            else:
                v_rect = pygame.Rect(650, 390, 50, 60)
            pygame.draw.rect(screen, VAULT_COLOR, v_rect, border_radius=8)
            draw_arabic_text("خزنة بنك", font, WHITE, screen, v_rect.x - 2, v_rect.y + 18)
            if player_rect.colliderect(v_rect):
                score_cash += 1000

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: p_x -= int(current_speed)
        if keys[pygame.K_RIGHT]: p_x += int(current_speed)
        if keys[pygame.K_UP] and on_ground:
            p_vy = -11
        
        draw_roblox_character(screen, p_x, p_y, BLUE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.update()
        clock.tick(60)

def create_mode():
    global current_color_index, current_conveyor_index
    placed_blocks = []
    placed_conveyors = []
    placed_lasers = []
    placed_worms = []
    placed_vaults = []
    custom_spawn = [80, 350]
    
    player_x, player_y = custom_spawn[0], custom_spawn[1]
    player_vy = 0
    player_exists = False
    
    tool_mode = "spawn_point"
    published_message_timer = 0
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill((25, 30, 42))
        
        publish_btn_rect = pygame.Rect(560, 15, 320, 40)
        pygame.draw.rect(screen, BLUE, publish_btn_rect, border_radius=8)
        draw_arabic_text("نشر مابك الجديد لكل اللاعبين", font, WHITE, screen, 575, 23)
        
        tool_btn_rect = pygame.Rect(130, 15, 415, 40)
        pygame.draw.rect(screen, (130, 40, 150), tool_btn_rect, border_radius=8)
        
        if tool_mode == "spawn_point":
            draw_arabic_text("الأداة: نقطة الريسبون (اضغط للتبديل)", font, SPAWN_COLOR, screen, 140, 23)
        elif tool_mode == "build_map":
            draw_arabic_text("الأداة: بناء المابات والجدران [C للون]", font, WHITE, screen, 150, 23)
        elif tool_mode == "conveyor_tool":
            conv_info = CONVEYOR_TYPES[current_conveyor_index]
            draw_arabic_text(f"الأداة: {conv_info['name']} [اضغط N للتغيير]", font, conv_info['color'], screen, 140, 23)
        elif tool_mode == "laser_security":
            draw_arabic_text("الأداة: ليزر برين روت الأمني القاتل", font, LASER_COLOR, screen, 145, 23)
        elif tool_mode == "worm_tool":
            draw_arabic_text("الأداة: دودة الماب العملاقة المرعبة", font, WORM_COLOR, screen, 150, 23)
        else:
            draw_arabic_text("الأداة: خزنة الأموال (ماب السرقة)", font, VAULT_COLOR, screen, 150, 23)
        
        draw_arabic_text("كليك شمال: بناء | كليك يمين: مسح | P: اختبار", font, WHITE, screen, 20, 12)
        draw_arabic_text(f"اللون [C]: {COLORS[current_color_index][0]}", font, COLORS[current_color_index][1], screen, 20, 45)
        
        if published_message_timer > 0:
            draw_arabic_text("يا بطل! تم نشر مابك بكل الأدوات في قائمة المابات بنجاح!", font, (0, 255, 120), screen, 220, 610)

        draw_arabic_text("ESC: رجوع", font, (180, 180, 180), screen, 20, 610)
        
        spawn_rect_draw = pygame.Rect(custom_spawn[0], custom_spawn[1] + 20, 40, 40)
        pygame.draw.rect(screen, SPAWN_COLOR, spawn_rect_draw, border_radius=8)
        draw_arabic_text("SPAWN", font, BLACK, screen, spawn_rect_draw.x + 2, spawn_rect_draw.y + 8)

        for block, color in placed_blocks:
            pygame.draw.rect(screen, color, block, border_radius=4)
        for conv in placed_conveyors:
            pygame.draw.rect(screen, conv['color'], conv['rect'], border_radius=6)
        for laser in placed_lasers:
            pygame.draw.rect(screen, LASER_COLOR, laser['rect'], border_radius=3)
        for worm in placed_worms:
            pygame.draw.rect(screen, WORM_COLOR, worm['rect'], border_radius=12)
            draw_arabic_text("دودة", font, WHITE, screen, worm['rect'].x + 5, worm['rect'].y + 8)
        for vault in placed_vaults:
            pygame.draw.rect(screen, VAULT_COLOR, vault, border_radius=8)
            
        if player_exists:
            player_vy += 0.5
            player_y += player_vy
            p_rect = pygame.Rect(player_x, player_y, 30, 60)
            
            if player_y > SCREEN_HEIGHT + 50:
                player_x, player_y = custom_spawn[0], custom_spawn[1]
                player_vy = 0

            for laser in placed_lasers:
                if p_rect.colliderect(laser['rect']):
                    player_x, player_y = custom_spawn[0], custom_spawn[1]
                    player_vy = 0

            for worm in placed_worms:
                if p_rect.colliderect(worm['rect']):
                    player_x, player_y = custom_spawn[0], custom_spawn[1]
                    player_vy = 0

            p_on_ground = False
            for block, color in placed_blocks:
                if p_rect.colliderect(block) and player_vy > 0:
                    player_y = block.y - 60
                    player_vy = 0
                    p_on_ground = True
                    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: player_x -= 4
            if keys[pygame.K_RIGHT]: player_x += 4
            if keys[pygame.K_UP] and p_on_ground:
                player_vy = -11
                
            draw_roblox_character(screen, player_x, player_y, BLUE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                if publish_btn_rect.collidepoint(mouse_x, mouse_y):
                    new_map = {
                        "name": f"ماب جديد ({len(PUBLISHED_MAPS) + 1}) - ماب مخصص",
                        "creator": "عبدالعزيز",
                        "spawn": list(custom_spawn),
                        "blocks": list(placed_blocks),
                        "conveyors": list(placed_conveyors),
                        "lasers": list(placed_lasers),
                        "worms": [ {"rect": pygame.Rect(w['rect']), "speed": w['speed'], "name": w['name']} for w in placed_worms ],
                        "vaults": list(placed_vaults),
                        "color": COLORS[current_color_index][1]
                    }
                    PUBLISHED_MAPS.append(new_map)
                    published_message_timer = 150
                
                elif tool_btn_rect.collidepoint(mouse_x, mouse_y):
                    if tool_mode == "spawn_point": tool_mode = "build_map"
                    elif tool_mode == "build_map": tool_mode = "conveyor_tool"
                    elif tool_mode == "conveyor_tool": tool_mode = "laser_security"
                    elif tool_mode == "laser_security": tool_mode = "worm_tool"
                    elif tool_mode == "worm_tool": tool_mode = "vault"
                    else: tool_mode = "spawn_point"
                
                elif mouse_y > 75:
                    clicked_rect = pygame.Rect(mouse_x - 30, mouse_y - 15, 100, 30)
                    if event.button == 1:
                        if tool_mode == "spawn_point":
                            custom_spawn = [mouse_x - 20, mouse_y - 30]
                            if not player_exists:
                                player_x, player_y = custom_spawn[0], custom_spawn[1]
                        elif tool_mode == "build_map":
                            placed_blocks.append((clicked_rect, COLORS[current_color_index][1]))
                        elif tool_mode == "conveyor_tool":
                            c_type = CONVEYOR_TYPES[current_conveyor_index]
                            placed_conveyors.append({"rect": pygame.Rect(mouse_x - 40, mouse_y - 10, 80, 24), "multiplier": c_type['multiplier'], "color": c_type['color'], "name": c_type['name']})
                        elif tool_mode == "laser_security":
                            placed_lasers.append({"rect": pygame.Rect(mouse_x - 10, mouse_y - 35, 15, 70), "name": "ليزر برين روت"})
                        elif tool_mode == "worm_tool":
                            placed_worms.append({"rect": pygame.Rect(mouse_x - 35, mouse_y - 20, 70, 35), "speed": 3.5, "name": "دودة"})
                        else:
                            placed_vaults.append(pygame.Rect(mouse_x - 25, mouse_y - 30, 50, 60))
                    elif event.button == 3:
                        for item in placed_blocks[:]:
                            if item[0].collidepoint(mouse_x, mouse_y): placed_blocks.remove(item)
                        for conv in placed_conveyors[:]:
                            if conv['rect'].collidepoint(mouse_x, mouse_y): placed_conveyors.remove(conv)
                        for laser in placed_lasers[:]:
                            if laser['rect'].collidepoint(mouse_x, mouse_y): placed_lasers.remove(laser)
                        for worm in placed_worms[:]:
                            if worm['rect'].collidepoint(mouse_x, mouse_y): placed_worms.remove(worm)
                        for vault in placed_vaults[:]:
                            if vault.collidepoint(mouse_x, mouse_y): placed_vaults.remove(vault)
                                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                elif event.key == pygame.K_c: current_color_index = (current_color_index + 1) % len(COLORS)
                elif event.key == pygame.K_n and tool_mode == "conveyor_tool":
                    current_conveyor_index = (current_conveyor_index + 1) % len(CONVEYOR_TYPES)
                elif event.key == pygame.K_p: player_exists = True

        pygame.display.update()
        clock.tick(60)

# تشغيل اللعبة
main_menu()