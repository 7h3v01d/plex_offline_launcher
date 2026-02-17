# Plex Offline Launcher

A family-friendly, self-hosted web client for your Plex Media Server, designed for full functionality during internet outages. It provides a personalized, multi-user GUI with separate watch histories, "On Deck" sections, and full media browsing capabilities.

Last Updated: August 24, 2025

## The Problem

Plex is fantastic, but its reliance on plex.tv for authentication can be a major issue. If your internet connection goes down, many Plex client apps are unable to sign in, effectively locking you out of your media library—even though the server is sitting on your local network.

### The Solution

This project provides a self-hosted web interface that runs directly on your Plex server. It uses Python and the Flask framework to connect to your Plex server's local API with a pre-authorised token, bypassing the need for an internet connection.

The application now supports multiple users, giving each family member their own personalized dashboard and watch history. It replicates the core Plex experience for a seamless and stable offline environment.

### Screenshot
!
(Image placeholder: A "Who's Watching?" screen with user profile icons)

### Features

- 👨‍👩‍👧‍👦 Family User Switching: A "Who's Watching?" screen lets each user select their profile for a personalized experience.

- ✅ Separate Watch Histories: "On Deck" and watched/unwatched status are unique to each user profile.

- 👍 Watched Status Control: Manually mark movies and episodes as watched or unwatched from the details page.

- ✨ Full-Featured GUI: A modern interface that feels like a real media client.

- 📡 Live Internet Status: Displays a clear "Online" or "Offline" indicator in the header.

- 🏠 Dynamic Homepage: Shows the logged-in user's On Deck (Continue Watching) and Recently Added media.

- ℹ️ Detailed Media Pages: Click any item to view its summary, artwork, rating, and cast.

- 📺 Full TV Show Browsing: Navigate from a show to its seasons and see a full episode list.

- 🔍 Integrated Search: A search bar in the header allows you to find any media in your library.

- 🌐 Network Accessible: Works from any phone, tablet, or computer on your local network.

---

### Requirements

- Python 3.x installed on the Plex server.
- pip for installing packages.
- An existing, configured Plex Media Server with at least one user profile.

---

## Installation & Setup
Follow these steps on your Plex server machine.

### 1. Create the Project Folder & Structure
Your project needs a templates sub-folder. The final structure should look like this:
```
plex-offline-launcher/
├── templates/
│   ├── base.html
│   ├── home_dashboard.html
│   ├── item_details.html
│   ├── player.html
│   ├── search_results.html
│   └── user_select.html
├── app.py
└── config.py
```
### 2. Install Dependencies
Install the required Python libraries using pip.

```Bash
pip install Flask python-plexapi requests
```

### 3. Configure the Application (config.py)
This file now requires two important pieces of information.

Part A: Plex Details

- PLEX_URL: Your server's local IP address and port (usually 32400).

- PLEX_TOKEN: The authentication token for the admin user. To find it:

1. In the Plex Web App, go to any item in your library.
2. Click the three-dot menu ... and select Get Info.
3. Click View XML and copy the token from the end of the new URL.


Part B: Secret Key for Sessions

SECRET_KEY: A random, secret string used to secure user sessions. This is required for user switching to work.

Your final config.py file should look like this:
```Python
# config.py
PLEX_URL = 'http://192.168.1.100:32400'  # 👈 REPLACE with your server's local URL
PLEX_TOKEN = 'YourPlexTokenHere'         # 👈 REPLACE with the admin token you copied
SECRET_KEY = 'any-random-long-string-of-characters-goes-here' # 👈 ADD THIS LINE
```
---

### 4. Add the Application Code
Copy and paste the code provided in our conversation into the corresponding files listed in the project structure above.

## Usage

### 1. Run the Application
Open a terminal, navigate to your plex-offline-launcher folder, and run the command:
```Bash
flask --app app run --host=0.0.0.0
```
### 2. Access and Navigate the Launcher

- Open a web browser on any device on your network and go to http://<your_server_ip>:5000.

      You will be greeted by the "Who's Watching?" screen.

- Select a user profile to access your personal dashboard.

      On any media details page, use the "Mark as Watched" / "Unwatched" buttons to manage your history.

To change profiles, click the "Switch User" link in the header.

### Troubleshooting

I can't connect from another device on the network.

---

This is almost always caused by a firewall on the server machine. <br> Your server's operating system (Windows, macOS, or Linux) is likely blocking incoming connections on port 5000.

>Solution: You need to add a new inbound rule to your server's firewall to allow incoming TCP traffic on port 5000.

## License
This project is licensed under the MIT License.
