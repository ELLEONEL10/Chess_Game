import os
import pygame
import webbrowser

pygame.init()
WIDTH = 700  
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess Game')
font_path = os.path.join('assets', 'font.otf')
font = pygame.font.Font(font_path, 22)  # Default font, smaller size
medium_font = pygame.font.Font(font_path, 30)  # Medium font for buttons
big_font = pygame.font.Font(font_path, 45)
fps = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Resources
RESOURCES_DIR = "assets"  # Base directory for assets
BG_PATH = os.path.join(RESOURCES_DIR, "images", "bg.png")  # Path to background image
def about_popup():
    """Display an about popup window."""
    popup_running = True
    popup_width, popup_height = 470, 150
    popup_x, popup_y = (WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2

    while popup_running:
        # Draw the popup
        popup = pygame.Surface((popup_width, popup_height))
        popup.fill(WHITE)
        pygame.draw.rect(popup, BLACK, popup.get_rect(), 3)

        # Add close button
        close_button = pygame.Rect(popup_width - 50, 20, 30, 40)
        pygame.draw.rect(popup, GRAY, close_button)
        pygame.draw.line(popup, BLACK, (close_button.x + 5, close_button.y + 5),
                         (close_button.x + close_button.width - 5, close_button.y + close_button.height - 5), 2)
        pygame.draw.line(popup, BLACK, (close_button.x + close_button.width - 5, close_button.y + 5),
                         (close_button.x + 5, close_button.y + close_button.height - 5), 2)

        # Add text and link
        text = font.render("Chess Game by Fadi Abbara & Anas Zahran", True, BLACK)
        link_text = font.render("github.com/ELLEONEL10/Chess_Game", True, (0, 0, 255))
        screen.blit(popup, (popup_x, popup_y))
        screen.blit(text, (popup_x + 20, popup_y + 60))
        screen.blit(link_text, (popup_x + 20, popup_y + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # Close button
                if close_button.collidepoint(mouse_pos[0] - popup_x, mouse_pos[1] - popup_y):
                    popup_running = False   
                
def main_menu():
    """Display the main menu."""
    running = True

    # Load background image
    background_img = pygame.image.load(BG_PATH).convert()

    # Button dimensions and positions
    button_width, button_height = 300, 50
    button_margin = 20
    buttons = {
        "Multiplayer": pygame.Rect((WIDTH - button_width) // 2, 300, button_width, button_height),
        "AI Game": pygame.Rect((WIDTH - button_width) // 2, 300 + button_height + button_margin, button_width, button_height),
        "About": pygame.Rect((WIDTH - button_width) // 2, 300 + 2 * (button_height + button_margin), button_width, button_height),
    }

    while running:
        # Draw the background
        screen.blit(background_img, (0, 0))

        # Draw buttons
        for label, rect in buttons.items():
            pygame.draw.rect(screen, BLACK, rect)  # Button background
            pygame.draw.rect(screen, WHITE, rect, 2)  # Button border
            text_surface = medium_font.render(label, True, WHITE)
            screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                                        rect.y + (rect.height - text_surface.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for label, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if label == "Multiplayer":
                            pygame.quit()  # Close the current Pygame window
                            import subprocess
                            subprocess.run(["python", "main.py"])
                            exit()  # Exit the current script
                        elif label == "AI Game":
                            pygame.quit()  # Close the current Pygame window
                            import subprocess
                            subprocess.run(["python", "chess/main.py"]) 
                            exit()  # Exit the current script
                        elif label == "About":
                            about_popup() 
if __name__ == "__main__":
    main_menu()


