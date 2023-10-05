import tkinter as tk
from tkinter import*
import ctypes
import random
from wonderwords import RandomWord as r
from PIL import Image, ImageTk

# Sharper window
ctypes.windll.shcore.SetProcessDpiAwareness(1)



class mainApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        # Setting up things for the game such as setting current game mode and letting timer know the game isn't running
        self.game = False
        self.randomMode = False
        self.title("Word Wizardry")
        self.geometry("1200x800")
        self.configure(bg='white')
        
        # Bind key touches to the function that reads the key typed
        self.bind('<Key>', self.userText)
        
        # Create the title, logo, timer logo, and initiate error count
        self.createMainWidgets()
        # Generate the first text passage in Normal mode
        self.generateText()
    
    def ToggleGamemode(self):
        # Change the game mode to the opposite of what it is set currently and clear screen because the widgets are different 
        if not self.game:
            self.randomMode = not self.randomMode
            if self.randomMode == True:
                # Clear screen 
                self.clearScreen()
                # Create the title, logo, timer logo, and initiate error count
                self.createMainWidgets()
                # Regenerate text passage to now be random words that pop up
                self.generateText()
                # Change the button to display the opposite game mode 
                self.switchGamemode.configure(text="Normal Mode")
            else:
                # Change the button to display opposite game mode
                self.switchGamemode.configure(text="randomMode Mode")
                # Clear screen 
                self.clearScreen()
                # Create the title, logo, timer logo, and initiate error count
                self.createMainWidgets()
                # Regenerate text passage to now be random words that pop up
                self.generateText()

    # Create the widgets that do not change based off game mode such as title, timer, logo and initiate error count
    def createMainWidgets(self):
        self.timer = Timer(self)
        
        self.titleLabel = Label(self, text="BQuon's Word Wizardry", fg='Black', font=('Consolas', 34), bg='white')
        self.titleLabel.place(relx=0.5, rely=0.07, anchor=N)
        
        self.switchGamemode = Button(self, text="Try Random Mode", font=('Consolas', 10),command=self.ToggleGamemode, fg='black', bg='lightgrey', activebackground='lightgrey')
        self.switchGamemode.place(relx=0.15, rely=0.25, anchor=CENTER)  # Add the button to the window
        
        self.logo = Image.open("wizardLogo.png")
        self.resized_logo = self.logo.resize((200,200))
        self.logoImage = ImageTk.PhotoImage(self.resized_logo)
        logoLabel = Label(self, image=self.logoImage, bd=0)
        logoLabel.place(relx=0.96, rely=0.15, anchor=E)
        
        self.errorCount = 0
   
    # Function to start game if not started and compare the letter typed to the letter in the word
    def userText(self, event=None):
        if not self.game:
            # Keep track of different score type for the random game mode 
            self.randomScore = 0
            self.randomCharacters = 0            
            # Letting the timer know the game has started and to call the Stop function after 60 seconds
            self.game = True 
            self.after(60000, self.stop)
            self.timer.updateTimer()
            
        try:
            # The wanted character in the word to type
            expected_char = self.leftToType.cget('text')[0]
            # Different comparison and updating widget display for the two game modes
            # Below would be normal mode
            if not self.randomMode:
                if (event.char == expected_char and self.game):
                    # Move the typed charater into the other widget and making the next character the new one to be typed
                    self.leftToType.configure(text=self.leftToType.cget('text')[1:])
                    self.alreadyTyped.configure(text=self.alreadyTyped.cget('text') + event.char)
                    # Display current letter needed to be typed
                    self.currentLetter.configure(text=self.leftToType.cget('text')[0])
                else:
                    # Increment the error count and update the widget display if user didn't type the expected character
                    self.errorCount += 1
                    self.displayErrorCount.configure(text=f'Error count: {self.errorCount}')
            else:
                # Random word mode
                if (event.char == expected_char and self.game):
                    # Move the typed charater into the other widget and making the next character the new one to be typed
                    self.leftToType.configure(text=self.leftToType.cget('text')[1:])
                    self.alreadyTyped.configure(text=self.alreadyTyped.cget('text') + event.char)
                    # Different measurement of accuracy tracking than normal mode
                    self.randomCharacters += 1
                    # If the user types the full word, add to score and generate another word
                    if len(self.leftToType.cget('text')) == 0:
                        self.alreadyTyped.configure(text='')
                        self.randomScore += 1
                        self.generateText()
                    # Display current letter needed to be typed
                    self.currentLetter.configure(text=self.leftToType.cget('text')[0])
                else:
                    # Increment the error count and update the widget display if user didn't type the expected character
                    self.errorCount += 1
                    self.displayErrorCount.configure(text=f'Error count: {self.errorCount}')          
        except tk.TclError:
            pass
                
    # Function to generate the text needed to be typed based on which game mode it currently is
    def generateText(self):
        # Normal mode text
        if not self.randomMode:
            possibleTexts = [
                "Computer Science is a dynamic field that drives innovation in technology. It encompasses the study of algorithms, data structures, and software development, with applications in various industries. One of the fundamental concepts in computer science is algorithms. Algorithms are step-by-step procedures for solving problems and performing tasks efficiently. They are the building blocks of software and play a crucial role in solving complex problems. Data structures are another vital aspect of computer science. They define how data is organized and stored in memory, affecting the efficiency and performance of algorithms. Common data structures include arrays, linked lists, and trees. Software development is at the core of computer science. Programmers use programming languages like Python, Java, and C++ to write software applications that range from mobile apps to web services. The development process involves designing, coding, testing, and debugging. Computer science is not limited to programming; it also encompasses areas like artificial intelligence, machine learning, and cybersecurity. These fields push the boundaries of what computers can achieve and are driving innovations in autonomous vehicles, natural language processing, and more. In summary, computer science is a dynamic and evolving field that underpins the modern digital age. It involves algorithms, data structures, software development, and emerging technologies that shape our world.",
                "Computer Science is the foundation of the digital world we live in today. It is the study of computers and computing technologies, covering a wide range of topics from hardware to software. In computer hardware, engineers design and build the physical components of computers, including processors, memory, and storage devices. These components are the heart of any computing system. Software development is a significant aspect of computer science. Programmers write code to create applications that run on computers and mobile devices. The software development process includes planning, coding, testing, and deployment. Computer scientists also explore the theory behind computation. They analyze algorithms, which are sets of instructions for solving problems, and study the limits of what computers can and cannot compute. Artificial intelligence (AI) is a cutting-edge field within computer science. AI systems can learn and make decisions, enabling applications like virtual assistants and self-driving cars. Computer science plays a crucial role in cybersecurity, as professionals work to protect data and systems from cyber threats. They develop security measures and protocols to safeguard information. In conclusion, computer science is a multifaceted field that encompasses hardware, software, theory, AI, and cybersecurity. It drives technological advancements that shape our digital world and continues to evolve as new challenges and opportunities emerge.",
                "Computer Science is the backbone of the modern technological landscape. It is a discipline that explores the principles, theories, and practices behind computing and information processing. One fundamental concept in computer science is programming. Programming languages like Python, Java, and C++ are tools that allow developers to instruct computers to perform tasks and solve problems. Learning to program is a key step in becoming a computer scientist. Algorithms are at the core of computer science. These are step-by-step instructions for solving problems efficiently. Designing efficient algorithms is crucial for tasks ranging from data sorting to optimizing search engines. Data structures are another essential component of computer science. They are ways of organizing and storing data for quick and efficient access. Examples include arrays, linked lists, and hash tables. Computer scientists also delve into the theoretical aspects of computation. They explore questions related to what can and cannot be computed, paving the way for new discoveries in areas like cryptography and quantum computing. The field of computer science extends beyond just programming and theory. It encompasses areas like database management, artificial intelligence, machine learning, and computer graphics. In summary, computer science is a diverse and dynamic field that drives innovation across industries. It encompasses programming, algorithms, data structures, theory, and cutting-edge technologies, making it an exciting and essential discipline in today's digital age."
            ]

            # Choosing a passage
            text = random.choice(possibleTexts).lower()

            self.alreadyTyped = Label(self, text=text[0:0], bg='white', fg='grey', font=('Consolas', 34))
            self.alreadyTyped.place(relx=0.5, rely=0.5, anchor=E)

            self.leftToType = Label(self, text=text[0:], bg='white', font=('Consolas', 34))
            self.leftToType.place(relx=0.5, rely=0.5, anchor=W)
            
            self.currentLetter = Label(self, text=text[0], bg='white', fg='grey', font=('Consolas', 24))
            self.currentLetter.place(relx=0.515, rely=0.55, anchor=N)
        else:
            # Generating random word from Wonderwords
            rw = r()
            text = rw.word()
            
            self.alreadyTyped = Label(self, text=text[0:0], bg='white', fg='grey', font=('Consolas', 34))
            self.alreadyTyped.place(relx=0.5, rely=0.5, anchor=E)

            self.leftToType = Label(self, text=text[0:], bg='white', font=('Consolas', 34))
            self.leftToType.place(relx=0.5, rely=0.5, anchor=W)
        
            self.currentLetter = Label(self, text=text[0], bg='white', fg='grey', font=('Consolas', 24))
            self.currentLetter.place(relx=0.515, rely=0.55, anchor=N)
        
        # Display error count
        self.displayErrorCount = Label(self, text=f'Error count: {self.errorCount}', bg='white', fg='red', font=('Consolas', 18))
        self.displayErrorCount.place(relx=0.5, rely=0.725, anchor=CENTER)

    # Function to handle what happens after the timer has ended    
    def stop(self):
        # Set the game to not running
        self.game = False
        
        # Different methods to displaying score based on game mode
        # Below is for normal mode
        if not self.randomMode:
            letterCount = len(self.alreadyTyped.cget('text'))
            wordCount = len(self.alreadyTyped.cget('text').split(' '))
            # Clear screen
            self.clearScreen()
            # Update the normal mode leaderboard
            self.updateLeaderboard("normalLeaderboard.txt", wordCount)
            
            # Display the updated leaderboard
            leaderboardText = "\n".join([f"{i + 1}. {score}" for i, score in enumerate(self.top5Scores)])
            leaderboard = Label(self, text="Top 5 Normal Mode Scores:\n " + leaderboardText, font=("Arial", 16), bg='white', highlightbackground="black", highlightthickness=2)
            leaderboard.place(relx=0.5, rely=0.17, anchor=CENTER)
            # Display the accuracy percent
            accuracyCalc = 100*(1-(self.errorCount/letterCount))
            accuracy = Label(self, text=f'Accuracy: {(accuracyCalc):.2f}%', bg='white',fg='black', font=('Consolas', 34))
            accuracy.place(relx=0.5, rely=0.5, anchor=CENTER)
            # Show how many words they typed
            result = Label(self, text=f'Words per minute: {wordCount}', bg='white',fg='black', font=('Consolas', 34))
            result.place(relx=0.5, rely=0.4, anchor=CENTER)
        # Below is for random mode
        else:
            # Clear screen
            self.clearScreen()
            # Show how many words they typed    
            result = Label(self, text=f'Words per minute: {self.randomScore}', bg='white', fg='black', font=('Consolas', 34))
            result.place(relx=0.5, rely=0.4, anchor=CENTER)
            # Update the random mode leaderboard
            self.updateLeaderboard("randomLeaderboard.txt", self.randomScore)
            
            # Display the updated leaderboard
            leaderboardText = "\n".join([f"{i + 1}. {score}" for i, score in enumerate(self.top5Scores)])
            leaderboard = Label(self, text="Top 5 Random Mode Scores:\n " + leaderboardText, font=("Arial", 16), bg='white', highlightbackground="black", highlightthickness=2)
            leaderboard.place(relx=0.5, rely=0.17, anchor=CENTER)
            # Display the accuracy percent
            accuracyCalc = 100*(1-(self.errorCount/self.randomCharacters))
            accuracy = Label(self, text=f'Accuracy: {(accuracyCalc):.2f}%', bg='white', fg='black', font=('Consolas', 34))
            accuracy.place(relx=0.5, rely=0.5, anchor=CENTER)
        # Display a restart button if user wants to play again
        restart = Button(self, text='Restart', command=self.restart, bg='white', fg ='red', font=('Consolas', 22))
        restart.place(relx=0.5, rely=0.7, anchor=CENTER)
    
    # Function to update leaderboard after game has ended
    def updateLeaderboard(self, filename, gamemodeScore):
        self.top5Scores = []
        # Read the files current top 5 scores
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                score = int(line.strip())
                self.top5Scores.append(score)
            # Append the most recent score and the stored scores and store the top 5 out of the 6
            self.top5Scores.append(gamemodeScore)
            self.top5Scores.sort(reverse=True)
            self.top5Scores = self.top5Scores[:5]
        # Rewrite the top 5 scores
        with open(filename, 'w') as file:
            for score in self.top5Scores:
                file.write(f"{score}\n")
        
    # Restart function that clears the screen, create the main widgets again and create text for the user to type    
    def restart(self):
        self.clearScreen()
        self.createMainWidgets()
        self.generateText()
        # Reset the timer
        self.timer = Timer(self)
        
    # Destroy current widgets displayed    
    def clearScreen(self):
        for widget in self.winfo_children():
            widget.destroy()
            

class Timer():
    def __init__(self, app) -> None:
        self.app = app
        self.timeLeft = 60
        # Label for the timer display
        self.timeLeftLabel = Label(self.app, text=f'{self.timeLeft} Seconds Left', bg='white', fg='black', font=('Consolas', 25))
        self.timeLeftLabel.place(relx=0.5, rely=0.4, anchor=S)
        
        self.updateTimer()
    
    def updateTimer(self):
        if self.timeLeft > 0 and self.app.game:
            self.timeLeft -= 1
            self.timeLeftLabel.configure(text=f'{self.timeLeft} Seconds Left')
            self.app.after(1000, self.updateTimer)
        elif self.timeLeft == 0:
            self.app.game = False
    
    
if __name__ == "__main__":
    app = mainApp()
    app.mainloop()