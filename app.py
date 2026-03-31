import streamlit as st
from PIL import Image, ImageDraw
import random
from io import BytesIO

# Page config
st.set_page_config(page_title="Flappy Bird", layout="centered", initial_sidebar_state="collapsed")

# Prevent scrolling
st.markdown("""
<style>
    body { overflow: hidden; }
    .main { overflow: hidden; height: 100vh; }
    [data-testid="stAppViewContainer"] { padding: 0; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "game_active" not in st.session_state:
    st.session_state.game_active = False
    st.session_state.bird_y = 200
    st.session_state.bird_velocity = 0
    st.session_state.pipes = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.flap_pressed = False

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_X = 50
BIRD_SIZE = 20
GRAVITY = 0.6
FLAP_STRENGTH = -12
PIPE_WIDTH = 50
PIPE_GAP = 120
PIPE_SPEED = 5

# Title and instructions
st.title("🐦 Flappy Bird")
st.markdown("**Press SPACE or ↑ Arrow to FLAP** | Press S to Start/Restart")

# JavaScript for keyboard control
st.markdown("""
<script>
document.addEventListener('keydown', function(event) {
  if (event.code === 'Space' || event.code === 'ArrowUp') {
    event.preventDefault();
    // Send flap signal via URL query params
    window.parent.postMessage({type: 'flap'}, '*');
  }
  if (event.code === 'KeyS') {
    event.preventDefault();
    window.parent.postMessage({type: 'start'}, '*');
  }
});
</script>
""", unsafe_allow_html=True)

# Control buttons - only show when game is not active to avoid button re-triggering
col1, col2, col3 = st.columns(3)

if not st.session_state.game_active:
    with col1:
        if st.button("Start Game (S)", key="start_btn"):
            st.session_state.game_active = True
            st.session_state.game_over = False
            st.session_state.bird_y = 200
            st.session_state.bird_velocity = 0
            st.session_state.pipes = []
            st.session_state.score = 0
            st.rerun()

if st.session_state.game_over:
    with col3:
        if st.button("Restart (R)", key="restart_btn"):
            st.session_state.bird_y = 200
            st.session_state.bird_velocity = 0
            st.session_state.pipes = []
            st.session_state.score = 0
            st.session_state.game_over = False
            st.rerun()

# Flap button (only interactive during gameplay, but hidden)
flap = False
if st.session_state.game_active and not st.session_state.game_over:
    # Space bar equivalent - using a checkbox to capture input
    with col2:
        if st.button("⬆️ FLAP", key="flap_btn"):
            flap = True

# Score display
st.metric("Score", st.session_state.score)

# Game loop simulation
if st.session_state.game_active and not st.session_state.game_over:
    # Apply gravity
    st.session_state.bird_velocity += GRAVITY
    st.session_state.bird_y += st.session_state.bird_velocity
    
    # Handle flap
    if flap:
        st.session_state.bird_velocity = FLAP_STRENGTH
    
    # Move pipes
    st.session_state.pipes = [[x - PIPE_SPEED, gap] for x, gap in st.session_state.pipes if x > -PIPE_WIDTH]
    
    # Add new pipe
    if len(st.session_state.pipes) == 0 or st.session_state.pipes[-1][0] < SCREEN_WIDTH - 150:
        gap_y = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        st.session_state.pipes.append([SCREEN_WIDTH, gap_y])
    
    # Collision detection
    if st.session_state.bird_y < 0 or st.session_state.bird_y + BIRD_SIZE > SCREEN_HEIGHT:
        st.session_state.game_over = True
    
    for pipe_x, gap_y in st.session_state.pipes:
        pipe_hitbox_left = pipe_x
        pipe_hitbox_right = pipe_x + PIPE_WIDTH
        bird_left = BIRD_X
        bird_right = BIRD_X + BIRD_SIZE
        bird_top = st.session_state.bird_y
        bird_bottom = st.session_state.bird_y + BIRD_SIZE
        
        if bird_right > pipe_hitbox_left and bird_left < pipe_hitbox_right:
            if bird_top < gap_y or bird_bottom > gap_y + PIPE_GAP:
                st.session_state.game_over = True
        
        # Scoring: bird passes pipe
        if pipe_x == BIRD_X - PIPE_SPEED:
            st.session_state.score += 1

# Render game frame as image
@st.cache_data
def create_cached_image():
    return Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), color="lightblue")

img = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), color="lightblue")
draw = ImageDraw.Draw(img)

# Draw pipes
for pipe_x, gap_y in st.session_state.pipes:
    # Top pipe
    draw.rectangle([pipe_x, 0, pipe_x + PIPE_WIDTH, gap_y], fill="green")
    # Bottom pipe
    draw.rectangle([pipe_x, gap_y + PIPE_GAP, pipe_x + PIPE_WIDTH, SCREEN_HEIGHT], fill="green")

# Draw bird
draw.ellipse([BIRD_X, st.session_state.bird_y, BIRD_X + BIRD_SIZE, st.session_state.bird_y + BIRD_SIZE], fill="yellow", outline="orange", width=2)

# Convert PIL image to bytes to avoid serialization issues
img_bytes = BytesIO()
img.save(img_bytes, format="PNG")
img_bytes.seek(0)

st.image(img_bytes, width=400)

# Game over message
if st.session_state.game_over:
    st.error(f"💀 Game Over! Final Score: {st.session_state.score}")

# Auto-rerun for game loop with a small delay to avoid excessive CPU
if st.session_state.game_active and not st.session_state.game_over:
    import time
    time.sleep(0.1)  # ~10 FPS instead of uncapped
    st.rerun()
