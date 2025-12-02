import streamlit as st
from config import set_page_config, apply_custom_styling, show_header, show_sidebar_user_info

set_page_config()
apply_custom_styling()

if 'user' not in st.session_state or not st.session_state.user:
    st.switch_page("pages/01_Login.py")

show_header()
show_sidebar_user_info(st.session_state.user)

st.markdown("---")
st.title("🎪 Waiting Room - Health & Entertainment")
st.markdown("### Explore Health Tools or Play Games!")

with st.sidebar:
    if st.button("⬅️ Back"):
        st.switch_page("pages/04_User_Dashboard.py")
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.user = None
        st.switch_page("pages/01_Login.py")

# Main menu
st.markdown("---")
st.markdown("### 🎯 Choose Your Path")

col1, col_space, col2 = st.columns([2, 1, 2])

with col1:
    st.markdown("## 💊 Blue Pill - Knowledge Portal")
    st.markdown("""
    **Health Calculators & Guides:**
    - 📏 BMI Calculator
    - 🍽️ Calorie Calculator  
    - 💧 Water Intake
    - 📚 Diet Guide
    - 🏃 Health Tips
    """)
    if st.button("📚 Enter Knowledge Portal", use_container_width=True):
        st.session_state.page = "knowledge"

with col2:
    st.markdown("## 🎮 Red Pill - Game Zone")
    st.markdown("""
    **Entertainment & Gaming:**
    - 🐍 Snake Game
    - 🎯 Score Tracking
    - 📊 Level System
    - 🏆 High Scores
    """)
    if st.button("🕹️ Enter Game Zone", use_container_width=True):
        st.session_state.page = "games"

# Knowledge Portal
if st.session_state.get("page") == "knowledge":
    st.markdown("---")
    st.title("💊 Knowledge Portal")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📏 BMI", "🍽️ Calories", "💧 Water", "📚 Diet", "🏃 Health"])
    
    # BMI Calculator
    with tab1:
        st.markdown("### 📏 BMI Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (kg)", min_value=1, max_value=500, value=70)
        
        with col2:
            height = st.number_input("Height (cm)", min_value=50, max_value=300, value=175)
        
        if st.button("Calculate BMI"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            
            st.success(f"✅ Your BMI: **{bmi:.2f}**")
            
            if bmi < 18.5:
                st.info("📊 Category: **Underweight**")
                st.markdown("Recommendation: Consult doctor for nutrition advice")
            elif 18.5 <= bmi < 25:
                st.success("📊 Category: **Normal Weight** ✅")
                st.markdown("Recommendation: Maintain your healthy lifestyle!")
            elif 25 <= bmi < 30:
                st.warning("📊 Category: **Overweight**")
                st.markdown("Recommendation: Increase exercise and reduce calorie intake")
            else:
                st.error("📊 Category: **Obese**")
                st.markdown("Recommendation: Consult healthcare provider immediately")
    
    # Calorie Calculator
    with tab2:
        st.markdown("### 🍽️ Daily Calorie Calculator (TDEE)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            weight_cal = st.number_input("Weight (kg) - Calorie", min_value=1, max_value=500, value=70)
        
        with col2:
            height_cal = st.number_input("Height (cm) - Calorie", min_value=50, max_value=300, value=175)
            gender = st.selectbox("Gender", ["Male", "Female"])
        
        activity = st.selectbox("Activity Level", {
            "Sedentary (little or no exercise)": 1.2,
            "Light (exercise 1-3 days/week)": 1.375,
            "Moderate (exercise 3-5 days/week)": 1.55,
            "Very Active (6-7 days/week)": 1.725,
            "Extremely Active": 1.9
        })
        
        if st.button("Calculate Daily Calories"):
            if gender == "Male":
                bmr = 88.362 + (13.397 * weight_cal) + (4.799 * height_cal) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight_cal) + (3.098 * height_cal) - (4.330 * age)
            
            tdee = bmr * activity
            
            st.success(f"✅ BMR: **{bmr:.0f}** kcal/day")
            st.success(f"✅ TDEE: **{tdee:.0f}** kcal/day")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"**Lose Weight:**\n{tdee - 500:.0f} kcal/day")
            with col2:
                st.info(f"**Maintain:**\n{tdee:.0f} kcal/day")
            with col3:
                st.info(f"**Gain Weight:**\n{tdee + 500:.0f} kcal/day")
    
    # Water Intake
    with tab3:
        st.markdown("### 💧 Daily Water Intake")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight_water = st.number_input("Weight (kg) - Water", min_value=1, max_value=500, value=70)
        
        with col2:
            activity_water = st.selectbox("Activity Level - Water", {
                "Sedentary": 1.0,
                "Moderate": 1.2,
                "High Activity": 1.5
            })
        
        if st.button("Calculate Water"):
            liters = weight_water * 0.033 * activity_water
            cups = liters * 4.22675
            
            st.success(f"✅ Daily Water: **{liters:.2f}** liters")
            st.info(f"💧 That's about **{cups:.0f}** cups per day")
            
            st.markdown("**💡 Hydration Tips:**")
            st.markdown("""
            - Drink water consistently throughout the day
            - More water needed if exercising or in hot climate
            - Morning: 1 glass after waking
            - Before meals: 1 glass
            - After exercise: Extra hydration
            """)
    
    # Diet Guide
    with tab4:
        st.markdown("### 📚 Balanced Diet Guide")
        
        st.markdown("**🍽️ Daily Meal Structure:**")
        st.markdown("""
        1. **Breakfast (7-8 AM)** - 400-500 kcal
           - Oats, eggs, fruits, whole grains
        
        2. **Mid-morning (10-11 AM)** - 100-150 kcal
           - Apple, nuts, yogurt
        
        3. **Lunch (1-2 PM)** - 600-700 kcal
           - Rice/roti, vegetables, protein
        
        4. **Afternoon (4-5 PM)** - 100-150 kcal
           - Tea, light snack
        
        5. **Dinner (7-8 PM)** - 500-600 kcal
           - Soup, vegetables, lean protein
        """)
        
        st.markdown("**🥗 Macronutrient Balance:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("**Protein: 25-30%**\nMeat, fish, eggs, legumes")
        with col2:
            st.info("**Carbs: 45-50%**\nWhole grains, rice, bread")
        with col3:
            st.warning("**Fats: 20-25%**\nOils, nuts, seeds")
    
    # Health Tips
    with tab5:
        st.markdown("### 🏃 Health & Wellness Tips")
        
        st.markdown("**💪 Exercise (150 mins/week):**")
        st.markdown("""
        - Cardio: 30 mins, 5 days/week
        - Strength: 3-4 sessions/week
        - Flexibility: Daily yoga/stretching
        """)
        
        st.markdown("**😴 Sleep (7-9 hours/night):**")
        st.markdown("""
        - Consistent sleep schedule
        - Cool, dark bedroom
        - No screens 1 hour before bed
        - Avoid caffeine after 2 PM
        """)
        
        st.markdown("**🧘 Stress Management:**")
        st.markdown("""
        - Meditation: 10-15 mins daily
        - Deep breathing exercises
        - Yoga practice
        - Social connection
        """)
    
    st.markdown("---")
    if st.button("⬅️ Back to Menu"):
        st.session_state.page = None
        st.rerun()

# Game Zone
elif st.session_state.get("page") == "games":
    st.markdown("---")
    st.title("🎮 Game Zone")
    
    st.markdown("### 🐍 Snake Game")
    
    st.markdown("""
    **How to Play:**
    - Use Arrow Keys to move
    - Eat red food to grow
    - Avoid hitting yourself
    - Press Space to pause
    - Get the highest score!
    """)
    
    st.markdown("**Controls:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("⬆️ **Up**")
    with col2:
        st.markdown("⬇️ **Down**")
    with col3:
        st.markdown("⬅️ **Left**")
    with col4:
        st.markdown("➡️ **Right**")
    
    # Snake Game HTML/CSS/JS
    st.markdown("""
    <style>
        canvas { border: 2px solid #00ff00; background: black; }
    </style>
    
    <canvas id="snakeCanvas" width="400" height="400"></canvas>
    
    <script>
        const canvas = document.getElementById('snakeCanvas');
        const ctx = canvas.getContext('2d');
        
        const gridSize = 20;
        const tileCount = 20;
        let snake = [{x: 10, y: 10}];
        let food = {x: 15, y: 15};
        let dx = 1, dy = 0;
        let score = 0;
        let paused = false;
        
        function drawGame() {
            ctx.fillStyle = 'black';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.strokeStyle = '#222';
            for(let i = 0; i <= tileCount; i++) {
                ctx.beginPath();
                ctx.moveTo(i * gridSize, 0);
                ctx.lineTo(i * gridSize, canvas.height);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(0, i * gridSize);
                ctx.lineTo(canvas.width, i * gridSize);
                ctx.stroke();
            }
            
            ctx.fillStyle = '#00ff00';
            snake.forEach((segment, index) => {
                if(index === 0) ctx.fillStyle = '#00aa00';
                ctx.fillRect(segment.x * gridSize + 1, segment.y * gridSize + 1, gridSize - 2, gridSize - 2);
                ctx.fillStyle = '#00ff00';
            });
            
            ctx.fillStyle = '#ff4444';
            ctx.fillRect(food.x * gridSize + 1, food.y * gridSize + 1, gridSize - 2, gridSize - 2);
            
            ctx.fillStyle = '#00ff00';
            ctx.font = '16px Arial';
            ctx.fillText('Score: ' + score, 10, canvas.height + 20);
        }
        
        function update() {
            if(!paused) {
                const head = {x: (snake[0].x + dx + tileCount) % tileCount, y: (snake[0].y + dy + tileCount) % tileCount};
                
                for(let segment of snake) {
                    if(head.x === segment.x && head.y === segment.y) {
                        alert('Game Over! Score: ' + score);
                        snake = [{x: 10, y: 10}];
                        score = 0;
                        dx = 1; dy = 0;
                    }
                }
                
                snake.unshift(head);
                
                if(head.x === food.x && head.y === food.y) {
                    score += 10;
                    food = {x: Math.floor(Math.random() * tileCount), y: Math.floor(Math.random() * tileCount)};
                } else {
                    snake.pop();
                }
            }
            
            drawGame();
            setTimeout(update, 100);
        }
        
        document.addEventListener('keydown', (e) => {
            if(e.key === 'ArrowUp' && dy === 0) {dx = 0; dy = -1;}
            if(e.key === 'ArrowDown' && dy === 0) {dx = 0; dy = 1;}
            if(e.key === 'ArrowLeft' && dx === 0) {dx = -1; dy = 0;}
            if(e.key === 'ArrowRight' && dx === 0) {dx = 1; dy = 0;}
            if(e.key === ' ') {e.preventDefault(); paused = !paused;}
        });
        
        update();
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("⬅️ Back to Menu"):
        st.session_state.page = None
        st.rerun()

# Default menu
if st.session_state.get("page") is None:
    st.markdown("---")
    st.info("👆 Choose a path above: Knowledge or Games!")

st.markdown("---")
st.markdown("**Version:** 2.0.0 | **Created:** December 2024")
