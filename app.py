import streamlit as st
import pandas as pd
import os
import json
import time
# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #fafafa, #f0f2f5);
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 80px !important;
    max-width: 700px;
}

.post-card {
    background: white;
    padding: 15px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
            /* INPUT FIELDS */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stFileUploader"] section,
div[data-testid="stRadio"] {
    border: 2px solid #ddd !important;
    border-radius: 12px !important;
    padding: 10px !important;
    background-color: #ffffff !important;
}

/* INPUT FOCUS (when user clicks) */
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border: 2px solid #fd1d1d !important;
    box-shadow: 0 0 6px rgba(253,29,29,0.3) !important;
}

/* BUTTONS (slightly toned down) */
div.stButton > button {
    background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500;
    height: 42px;
}

/* BUTTON HOVER */
div.stButton > button:hover {
    opacity: 0.9;
    transform: scale(1.02);
}

/* LABELS */
label {
    font-weight: 500 !important;
    color: #333 !important;
}

.username {
    font-weight: 600;
}

.navbar-top {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 55px;
    background: white !important;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 15px;
    border-bottom: 1px solid #ddd;
}
.dp {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    object-fit: cover;
}
.dp-small {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    object-fit: cover;
}
img {
    border-radius: 50%;
}  
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.brand {
    font-family: 'Pacifico', cursive;
    background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

/* different sizes for reuse */
.brand-large {
    font-size: 42px;
}

.brand-small {
    font-size: 26px;
}
button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #ddd !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

button:hover {
    background-color: #f2f2f2 !important;
    color: black !important;
}
header {
    visibility: hidden !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden;
}            
div[data-testid="stTextInput"] input {
    border-radius: 20px !important;
    padding: 10px !important;
}                                         
</style>
""", unsafe_allow_html=True)

# ---------------- FILE SETUP ----------------
os.makedirs("data", exist_ok=True)
os.makedirs("images", exist_ok=True)

users_file = "data/users.csv"
posts_file = "data/posts.csv"

if not os.path.exists(users_file):
    pd.DataFrame(columns=["username","password","dp","insta_name","following","private"]).to_csv(users_file,index=False)

if not os.path.exists(posts_file):
    pd.DataFrame(columns=["username","image_path","caption","likes","comments"]).to_csv(posts_file,index=False)

users = pd.read_csv(users_file)
posts = pd.read_csv(posts_file)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "show_login" not in st.session_state:
    st.session_state["show_login"] = False    
if "user" not in st.session_state:

    st.markdown("""
    <style>
    .logo-box {
       width: 90px;
       height: 90px;
       margin: auto;
       border-radius: 25px;
       background: radial-gradient(circle at 30% 107%, 
          #fdf497 0%, #fdf497 5%, 
          #fd5949 45%, #d6249f 60%, 
          #285AEB 90%);
       display: flex;
       align-items: center;
       justify-content: center;
    }
    .logo-inner {
       width: 45px;
       height: 45px;
       border: 3px solid white;
       border-radius: 12px;
       position: relative;
    }
    .logo-inner::before {
       content: "";
       width: 20px;
       height: 20px;
       border: 3px solid white;
       border-radius: 50%;
       position: absolute;
       top: 8px;
       left: 8px;
    }
    .logo-inner::after {
       content: "";
       width: 6px;
       height: 6px;
       background: white;
       border-radius: 50%;
       position: absolute;
       top: 4px;
       right: 4px;
    }
    .app-name {
       text-align: center;
       font-size: 42px;
       font-weight: bold;
       margin-top: 15px;
    }

    .tagline {
       text-align: center;
       color: gray;
       font-size: 16px;
       margin-top: 8px;
    }                              
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:10px; text-align:center;">
    <div class="logo-box">
    <div class="logo-inner"></div>
    </div>
    
    <div class="brand brand-large">ReelGramm</div>            
    <div class="tagline">Want to have a ride to the reel world? 🚀</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state["show_login"]:
      if st.button("Get Started 🚀"):
        st.session_state["show_login"] = True
        st.rerun()
    # ---------------- LOGIN SIDEBAR ---------------- 
    st.markdown("""
    <style>
    div.stButton > button {
       background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
       color: white !important;
       border: none !important;
       border-radius: 12px !important;
       font-weight: 600;
       height: 45px;
    }
    div.stButton > button:hover {
       opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.session_state.get("show_login"):
        st.title("Login / Signup")
        colA, colB = st.columns(2)
        if "auth_mode" not in st.session_state:
            st.session_state["auth_mode"] = "Login"

        with colA:
            if st.button("Login", use_container_width=True):
                st.session_state["auth_mode"] = "Login"
                st.rerun()

        with colB:
            if st.button("Signup", use_container_width=True):
               st.session_state["auth_mode"] = "Signup"
               st.rerun()

        choice = st.session_state["auth_mode"]
            
    # ---------------- LOGIN ----------------
        if choice == "Login":
                st.markdown("### Login")
                username = st.text_input("Username", key="login_user")
                password = st.text_input("Password", type="password", key="login_pass")
                if st.button("Login 🚀", use_container_width=True):
                    row = users[users["username"] == username]
                    if not row.empty and row.iloc[0]["password"] == password:
                       st.session_state["user"] = username
                       st.session_state["page"] = "home"
                       st.rerun()
                    else:
                       st.error("Invalid login ❌")
# ---------------- SIGNUP ----------------
        elif choice == "Signup":
                st.markdown("### Create Account")
                insta_name = st.text_input("Name", key="signup_name")
                username = st.text_input("Username", key="signup_user")
                password = st.text_input("Password", type="password", key="signup_pass")         
                dp_file = st.file_uploader("Upload DP", type=["jpg","png"], key="signup_dp")
                account_type = st.radio("Account Type", ["Public", "Private"])
                if st.button("Create Account 🚀", use_container_width=True):
                    if username not in users["username"].values:
                        dp_path = ""
                        if dp_file:
                            filename = dp_file.name.replace(" ", "_")
                            dp_path = f"images/{int(time.time())}_{filename}"
                            with open(dp_path, "wb") as f:
                                f.write(dp_file.getbuffer())

                        is_private = True if account_type == "Private" else False

                        new = pd.DataFrame([[username, password, dp_path, insta_name, json.dumps([]), is_private]],columns=users.columns)

                        users = pd.concat([users, new])
                        users.to_csv(users_file, index=False)

                        st.success("Account created ✅")
                    else:
                        st.error("Username already exists ❌")

    
                st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------- FUNCTIONS ----------------
def get_following(username):
    row = users[users["username"] == username]
    if not row.empty:
        try:
            return json.loads(row.iloc[0]["following"])
        except:
            return []
    return []
def get_followers(target_user):
    count = 0
    for _, row in users.iterrows():
        try:
            following = json.loads(row["following"])
        except:
            following = []
        if target_user in following:
            count += 1
    return count

def get_following_count(username):
    return len(get_following(username))

def toggle_follow(current_user, target_user):
    idx = users[users["username"] == current_user].index[0]
    following = get_following(current_user)

    if target_user in following:
        following.remove(target_user)
    else:
        following.append(target_user)

    users.at[idx, "following"] = json.dumps(following)
    users.to_csv(users_file, index=False)

def can_view_profile(current_user, target_user):
    target_row = users[users["username"] == target_user]

    if target_row.empty:
        return False

    is_private = bool(target_row.iloc[0]["private"])

    # ✅ If account is PUBLIC → always visible
    if not is_private:
        return True

    # ✅ If account is PRIVATE → only visible if following
    following = get_following(current_user)

    return target_user in following
# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar-top">
<div style="font-size:20px;">➕</div>
<div class="brand brand-small">ReelGramm</div>
<div style="font-size:20px;">🤍</div>
</div>
""", unsafe_allow_html=True)

# ---------------- HOME ----------------
if st.session_state["page"] == "home":

    for i, row in posts.iloc[::-1].iterrows():
        st.markdown('<div class="post-card">', unsafe_allow_html=True)

        name = row["username"]
        user_data = users[users["username"] == row["username"]]
        if not user_data.empty:
            name = user_data.iloc[0]["insta_name"] or row["username"]

        col1, col2 = st.columns([1,6])
        with col1:
            if not user_data.empty:
                dp_path = str(user_data.iloc[0]["dp"]).strip()
                if dp_path and os.path.exists(dp_path):
                    st.image(dp_path, width=45)
                else:
                    st.write("👤")
            else:
                st.write("👤")
        with col2:
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px;">
                <div style="font-weight:600;">@{name}</div>
                </div>
            """, unsafe_allow_html=True)
        if os.path.exists(str(row["image_path"])):
            st.image(row["image_path"], use_container_width=True)

        st.write(f"❤️ {row['likes']} likes")

        col1, col2, col3 = st.columns([1,1,6])
        with col1:
            if st.button("❤️", key=f"like_{i}"):
               posts.at[i,"likes"] += 1
               posts.to_csv(posts_file,index=False)
               st.rerun()
        with col2:
            if st.button("💬", key=f"c_{i}"):
                st.session_state["page"] = "comments"
                st.session_state["selected_post"] = i
                st.rerun()
        st.markdown("<hr style='border:0.5px solid #eee;'>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
# ---------------- COMMENTS ----------------
elif st.session_state["page"] == "comments":

    i = st.session_state.get("selected_post")
 
    row = posts.loc[i]

    if os.path.exists(str(row["image_path"])):
        st.image(row["image_path"])

    st.markdown(f"""
       <div class="caption">
       <b>{row['username']}</b> {row['caption']}
       </div>
       """, unsafe_allow_html=True)

    try:
        comments = json.loads(row["comments"])
    except:
        comments = []

    for c in comments[::-1]:
        st.write(c)

    new = st.text_input("Add comment")

    if st.button("Post"):
        if new.strip():
            comments.append(f"{st.session_state['user']}: {new}")
            posts.at[i,"comments"] = json.dumps(comments)
            posts.to_csv(posts_file,index=False)
            st.rerun()

    if st.button("⬅ Back"):
        st.session_state["page"] = "home"
        st.rerun()

# ---------------- PROFILE ----------------
elif st.session_state["page"] == "profile":

    current_user = st.session_state["user"]
    # ---------------- PROFILE HEADER ----------------
    followers = get_followers(current_user)
    following = get_following_count(current_user)
    user_posts = posts[posts["username"] == current_user]

    user_row = users[users["username"] == current_user]
    idx = user_row.index[0]
    current_dp = user_row.iloc[0]["dp"]
    insta_name = user_row.iloc[0]["insta_name"] or current_user
    col1, col2 = st.columns([1,3])

    with col1:
        if current_dp and os.path.exists(current_dp):
           st.image(current_dp, width=90)
        else:
           st.write("👤")

    with col2:
        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button(f"{len(user_posts)}\nPosts", key="my_posts_btn"):
               st.session_state["view_user"] = current_user
               st.session_state["page"] = "profile" 
        with c2:
            if st.button(f"{followers}\nFollowers", key="my_followers_btn"):
                st.session_state["view_user"] = current_user
                st.session_state["page"] = "followers"
                st.rerun()
        with c3:
            if st.button(f"{following}\nFollowing"):
               st.session_state["page"] = "following"
               st.rerun()
    if st.button("⬅ Back", key="back_profile"):
       st.session_state["page"] = "home"
       st.rerun()           
    # ---------------- DP SECTION ----------------
    st.markdown("### DP UPLOAD")


    # Upload new DP
    new_dp = st.file_uploader("Upload new DP", type=["jpg","png"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Update DP"):
            if new_dp:
                filename = new_dp.name.replace(" ", "_")
                path = f"images/{int(time.time())}_{filename}"

                with open(path, "wb") as f:
                    f.write(new_dp.getbuffer())

                users.at[idx, "dp"] = path
                users.to_csv(users_file, index=False)

                st.success("DP updated!")
                st.rerun()

    with col2:
        if current_dp and st.button("Delete DP"):
            users.at[idx, "dp"] = ""
            users.to_csv(users_file, index=False)

            st.success("DP removed!")
            st.rerun()

    # ---------------- POSTS SECTION ----------------
    st.markdown("---")
    st.subheader("Posts")

    if user_posts.empty:
        st.write("No posts yet 😔")
    else:
        cols = st.columns(3)
        posts_list = user_posts.iloc[::-1].reset_index()
        for i, row in posts_list.iterrows():
            col = cols[i % 3]

            with col:
                path = str(row["image_path"]).strip()
  
                if path and os.path.exists(path):
                    st.image(path, width="stretch")

                    if st.button("open", key=f"post_click_{i}"):
                       st.session_state["page"] = "view_post"
                       st.session_state["selected_post"] = row["index"]
                       st.rerun()
    # ---------------- BACK ----------------
    if st.button("⬅ Back"):
        st.session_state["page"] = "home"
        st.rerun()

# ---------------- SEARCH ----------------
elif st.session_state["page"] == "search":

    st.subheader("Search")

    # INIT STATE
    if "search_done" not in st.session_state:
        st.session_state["search_done"] = False
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""

    col1, col2 = st.columns([6,1])

    with col1:
        query = st.text_input("Search",placeholder="Search users",key="search_input",label_visibility="collapsed")

    with col2:
        if st.button("🔍"):
            st.session_state["search_done"] = True
            st.session_state["search_query"] = query

    # RUN SEARCH FROM STATE (NOT BUTTON)
    if st.session_state["search_done"]:

        query = st.session_state["search_query"]

        if not query.strip():
            st.warning("Type something to search 😅")

        else:
            results = users[
                users["username"].str.contains(query, case=False, na=False) |
                users["insta_name"].str.contains(query, case=False, na=False)
            ]

            if results.empty:
                st.warning("No user found 😔")

            else:
                for _, row in results.iterrows():

                    target_user = row["username"]

                    col1, col2 = st.columns([1,6])

                    with col1:
                        if row["dp"] and os.path.exists(row["dp"]):
                            st.image(row["dp"], width=40)
                        else:
                            st.write("👤")

                    with col2:
                        if st.button(
                            f"{row['insta_name'] or row['username']}",
                            key=f"user_click_{target_user}"
                        ):
                            st.session_state["target_profile"] = target_user

                            if can_view_profile(st.session_state["user"], target_user):
                                st.session_state["page"] = "view_profile"
                            else:
                                st.session_state["page"] = "private_profile"

                            st.rerun()

    # BACK
    if st.button("⬅ Back"):
        st.session_state["search_done"] = False
        st.session_state["page"] = "home"
        st.rerun()
# ---------------- NEW POST ----------------
elif st.session_state["page"] == "new_post":

    st.subheader("Create Post")

    img = st.file_uploader("Upload Image", type=["jpg","png"])
    caption = st.text_area("Write caption")

    if st.button("Post"):
        if img and caption:

            filename = img.name.replace(" ", "_")
            path = f"images/{int(time.time())}_{filename}"

            with open(path, "wb") as f:
                f.write(img.getbuffer())

            new_post = pd.DataFrame(
                [[st.session_state["user"], path, caption, 0, json.dumps([])]],
                columns=["username","image_path","caption","likes","comments"]
            )

            posts = pd.concat([posts, new_post], ignore_index=True)
            posts.to_csv(posts_file, index=False)

            st.success("Posted successfully!")

            st.session_state["page"] = "home"
            st.rerun()

        else:
            st.warning("Upload image + caption")

    if st.button("⬅ Back"):
        st.session_state["page"] = "home"
        st.rerun()
#--------followers-------        
elif st.session_state["page"] == "followers":
    current_user = st.session_state.get("view_user")
    st.subheader("Followers")
    found = False
    for _, row in users.iterrows():
        try:
           following = json.loads(row["following"])
        except:
           following = []
        if current_user in following:
           st.write(f"@{row['username']}")
           found = True
    if not found:
        st.write("No followers yet 😔")
    if st.button("⬅ Back", key="back_followers"):
      if st.session_state.get("view_user") == st.session_state["user"]:
        st.session_state["page"] = "profile"   # my profile
      else:
        st.session_state["page"] = "view_profile"  # Y profile
      st.rerun()  
#------following----------------
elif st.session_state["page"] == "following":
    current_user = st.session_state.get("view_user")
    st.subheader("Following")
    following_list = get_following(current_user)
    if not following_list:
       st.write("Not following anyone yet 😔")
    else:
       for user in following_list:
        st.write(f"@{user}")

    if st.button("⬅ Back", key="back_following"):
      if st.session_state.get("view_user") == st.session_state["user"]:
        st.session_state["page"] = "profile"
      else:
        st.session_state["page"] = "view_profile"
      st.rerun()  
#---------POSTS---------------------          
elif st.session_state["page"] == "view_post":

    i = st.session_state.get("selected_post")

    if i is None:
        st.write("No post selected")
    else:
        row = posts.loc[i]

        # Image
        path = str(row["image_path"]).strip()
        if path and os.path.exists(path):
            st.image(path, width="stretch")

        # Caption
        st.markdown(f"**{row['username']}** {row['caption']}")

        # Likes
        st.write(f"❤️ {row['likes']} likes")

        # Like button
        if st.button("❤️ Like"):
            posts.at[i, "likes"] += 1
            posts.to_csv(posts_file, index=False)
            st.rerun()

        # Comments
        st.markdown("### Comments")

        try:
            comments = json.loads(row["comments"])
        except:
            comments = []

        for c in comments[::-1]:
            st.write(c)

        new_comment = st.text_input("Add comment")

        if st.button("Post Comment"):
            if new_comment.strip():
                comments.append(f"{st.session_state['user']}: {new_comment}")
                posts.at[i, "comments"] = json.dumps(comments)
                posts.to_csv(posts_file, index=False)
                st.rerun()

    if st.button("⬅ Back", key="back_post"):
       st.session_state["page"] = "profile"
       st.rerun() 

#-----------Private----------
elif st.session_state["page"] == "private_profile":
    
    target_user = st.session_state["target_profile"]
    row = users[users["username"] == target_user].iloc[0]

    followers = get_followers(target_user)
    following = get_following_count(target_user)
    user_posts = posts[posts["username"] == target_user]

    col1, col2 = st.columns([1,3])

    # DP
    with col1:
        if row["dp"] and os.path.exists(row["dp"]):
            st.image(row["dp"], width=90)
        else:
            st.write("👤")

    # STATS (NOT clickable)
    with col2:
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**{len(user_posts)}**  \nPosts")
        c2.markdown(f"**{followers}**  \nFollowers")
        c3.markdown(f"**{following}**  \nFollowing")

    st.markdown(f"### @{target_user}")
    current_user = st.session_state["user"]

    if can_view_profile(current_user, target_user):
       st.session_state["page"] = "view_profile"
       st.rerun()
    is_following = target_user in get_following(current_user)
    if is_following:
        if st.button("Unfollow", key=f"unfollow_private_{target_user}"):
           toggle_follow(current_user, target_user)
           st.rerun()
    else:
        if st.button("Follow", key=f"follow_private_{target_user}"):
           toggle_follow(current_user, target_user)
           st.session_state["page"] = "view_profile"
           st.rerun()

    # 🔒 PRIVATE BOX (clean like Insta)
    st.markdown("""
    <div style="
        margin-top:20px;
        padding:15px;
        border-radius:12px;
        background:#1e1e1e;
        color:white;
        text-align:center;
    ">
        🔒 Private account <br>
        Follow this account to see their posts
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅ Back", key="back_private"):
       st.session_state["page"] = "search"
       st.rerun()

#------------Public-----------------------------
elif st.session_state["page"] == "view_profile":

    target_user = st.session_state["target_profile"]

    user_posts = posts[posts["username"] == target_user]
    row = users[users["username"] == target_user].iloc[0]

    col1, col2 = st.columns([1,3])
    # DP
    with col1:
        if row["dp"] and os.path.exists(row["dp"]):
          st.image(row["dp"], width=90)
        else:
          st.write("👤")
    # STATS (CLICKABLE like real insta)
    with col2:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(f"{len(user_posts)}\nPosts", key=f"posts_{target_user}"):
                st.session_state["view_user"] = target_user
                st.session_state["page"] = "view_profile" 
        with c2:
            if st.button(f"{get_followers(target_user)}\nFollowers"):
               st.session_state["view_user"] = target_user
               st.session_state["page"] = "followers"
               st.rerun()
        with c3:
            if st.button(f"{get_following_count(target_user)}\nFollowing"):
               st.session_state["view_user"] = target_user
               st.session_state["page"] = "following"
               st.rerun()
    # USERNAME BELOW
    st.markdown(f"### @{target_user}")
    current_user = st.session_state["user"]
    is_following = target_user in get_following(current_user)
    if is_following:
        if st.button("Unfollow", key=f"unfollow_{target_user}"):
           toggle_follow(current_user, target_user)
           st.rerun()
    else:
        if st.button("Follow", key=f"follow_{target_user}"):
           toggle_follow(current_user, target_user)
           st.rerun()

    st.subheader("Posts")

    for _, p in user_posts.iterrows():
        if os.path.exists(p["image_path"]):
            st.image(p["image_path"], use_container_width=True)
            st.write(p["caption"])

    if st.button("⬅ Back", key="back_public"):
       st.session_state["page"] = "search"
       st.rerun()
# ---------------- NAV ----------------
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠"):
        st.session_state["page"] = "home"
        st.rerun()

with col2:
    if st.button("➕"):
        st.session_state["page"] = "new_post"
        st.rerun()

with col3:
    if st.button("👤", key="nav_profile"):
        st.session_state["page"] = "profile"
        st.rerun()

with col4:
    if st.button("🔍", key="nav_search"):
        st.session_state["page"] = "search"
        st.rerun()
