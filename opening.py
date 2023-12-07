import tkinter as tk
import random
from tkinter  import *
import random
import datetime
import time as t  
import threading  

class Baccarat:
    def __init__(self, master):
        self.master = master
        self.master.title("Baccarat")
        self.master.geometry("1400x800")

        self.start_screen()

    def start_screen(self):
        self.start_canvas = tk.Canvas(self.master, width=1400, height=800)
        self.start_canvas.pack()
        self.start_bg_image = tk.PhotoImage(file='startbg.png')  
        self.start_canvas.create_image(0, 0, anchor='nw', image=self.start_bg_image)

        self.start_button = tk.Button(self.master, text="게임 시작", command=self.start_game, font=("Helvetica", 30), width=10, height=3, bg="skyblue")
        self.start_button.place(x=570, y=600)

    def start_game(self):
        self.start_button.destroy()
        self.start_canvas.destroy()


        self.canvas = tk.Canvas(self.master, width=1400, height=800)
        self.canvas.pack()
        self.background_image = tk.PhotoImage(file='cardbg.png')  
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_image)

        self.user_funds = 2000
        self.bet_amount = 0
        self.bet_type = ""

        self.player_card_label = tk.Label(self.master, text="Player's Card:")
        self.player_card_label.place_forget() 

        self.player_card_values = []
        self.player_card_labels = []

        self.banker_card_label = tk.Label(self.master, text="Banker's Card:")
        self.banker_card_label.place_forget() 

        self.banker_card_values = []
        self.banker_card_labels = []

        self.result_label = tk.Label(self.master, text="", font=("Helvetica", 50), bg='green',fg="black")
        self.result_label.place(x=520, y=310)  

        self.funds_label = tk.Label(self.master, text=f"보유 코인: {self.user_funds}", font=("Helvetica", 20), bg='green')
        self.funds_label.place(x=600, y=50)  

        self.bet_label = tk.Label(self.master, text="투자 코인 입력", font=("Helvetica", 20), bg='green')
        self.bet_label.place(x=612, y=510)  

        self.bet_entry = tk.Entry(self.master, font=("Helvetica", 30), width=10)
        self.bet_entry.place(x=592, y=570)   

        self.play_button = tk.Button(self.master, text="Play", command=self.play, font=("Helvetica", 15), width=20, height=5, bg="skyblue")
        self.play_button.place(x=590, y=650)

        self.player_button = tk.Button(self.master, text="강냉이", command=lambda: self.place_bet("player"), font=("Helvetica", 15,'bold'), width=20, height=5, bg="red")
        self.player_button.place(x=100, y=650)

        self.banker_button = tk.Button(self.master, text="람브", command=lambda: self.place_bet("banker"), font=("Helvetica", 15,'bold'), width=20, height=5, bg="yellow")
        self.banker_button.place(x=1100, y=650) 

        self.images = []  
        self.winner_image_label = None

    def place_bet(self, bet_type):
        try:
            self.bet_amount = self.get_bet_amount()

            if self.bet_amount <= 0 or self.bet_amount > self.user_funds:
                raise ValueError("Invalid bet amount")

            self.bet_type = bet_type
            if self.bet_type == "player":
                self.result_label.config(text="강냉이 선택")
            else:
                self.result_label.config(text=" 람브 선택 ")
        except ValueError as e:
            self.result_label.config(text=str(e))

    def play(self):
        try:
            if self.bet_amount <= 0 or self.bet_amount > self.user_funds:
                raise ValueError("Invalid bet amount")

            self.reset_game()

            self.player_card_values = [self.get_card() for _ in range(2)]
            for index, (value, image) in enumerate(self.player_card_values):
                label = tk.Label(self.master, image=image)
                label.image = image  
                label.place(x=150 + index * 100, y=100)
                self.player_card_labels.append(label)

            self.banker_card_values = [self.get_card() for _ in range(2)]
            for index, (value, image) in enumerate(self.banker_card_values):
                label = tk.Label(self.master, image=image)
                label.image = image  
                label.place(x=950 + index * 100, y=100)
                self.banker_card_labels.append(label)

            self.user_funds -= self.bet_amount
            self.funds_label.config(text=f"보유 코인: {self.user_funds}")

            self.apply_rules()

        except ValueError as e:
            self.result_label.config(text=str(e))

    def apply_rules(self):
        player_sum = sum(value for value, image in self.player_card_values) % 10
        banker_sum = sum(value for value, image in self.banker_card_values) % 10

        if (player_sum >= 8 or banker_sum >= 8) or \
           (player_sum in [6, 7] and banker_sum in [6, 7]):
            self.determine_winner()
            return

        if player_sum <= 5:
            card = self.get_card()
            self.player_card_values.append(card)
            label = tk.Label(self.master, image=card[1])
            label.image = card[1]
            label.place(x=50 + len(self.player_card_values) * 100, y=400)
            self.player_card_labels.append(label)
            player_sum = sum(value for value, image in self.player_card_values) % 10

        if len(self.player_card_values) == 3:
            if banker_sum <= 2 or \
               (banker_sum == 3 and self.player_card_values[-1][0] != 8) or \
               (banker_sum == 4 and self.player_card_values[-1][0] not in [0, 1, 8, 9]) or \
               (banker_sum == 5 and self.player_card_values[-1][0] not in [0, 1, 2, 3, 8, 9]) or \
               (banker_sum == 6 and self.player_card_values[-1][0] not in [0, 1, 2, 3, 4, 5, 8, 9]):
                card = self.get_card()
                self.banker_card_values.append(card)
                label = tk.Label(self.master, image=card[1])
                label.image = card[1]
                label.place(x=850 + len(self.banker_card_values) * 100, y=400)
                self.banker_card_labels.append(label)

        elif banker_sum <= 5:
            card = self.get_card()
            self.banker_card_values.append(card)
            label = tk.Label(self.master, image=card[1])
            label.image = card[1]
            label.place(x=750 + len(self.banker_card_values) * 100, y=400)
            self.banker_card_labels.append(label)

        self.determine_winner()

    def get_card(self):
        original_value = random.randint(1, 13)
        card_value = original_value if original_value <= 10 else 0
        card_image = f"card{original_value}.png"
        image = tk.PhotoImage(file=card_image)
        self.images.append(image)
        return card_value, image

    def get_bet_amount(self):
        try:
            bet_amount = int(self.bet_entry.get())
            if bet_amount <= 0:
                raise ValueError("Bet amount must be greater than 0")
            return bet_amount
        except ValueError:
            raise ValueError("Invalid bet amount")

    def reset_game(self):
        for label in self.player_card_labels:
            label.destroy()
        self.player_card_values = []
        self.player_card_labels = []

        for label in self.banker_card_labels:
            label.destroy()
        self.banker_card_values = []
        self.banker_card_labels = []

        #self.result_label.config(text="") 
        if self.winner_image_label is not None:  # 승리 이미지 레이블이 있으면 제거
            self.winner_image_label.destroy()
            self.winner_image_label = None

    def determine_winner(self):
        player_sum = sum(value for value, image in self.player_card_values) % 10
        banker_sum = sum(value for value, image in self.banker_card_values) % 10

        if player_sum > banker_sum:
            self.result_label.config(text="강냉이 Wins!", fg="red")
            if self.bet_type == "player":
                self.user_funds += self.bet_amount * 2
            self.show_winner_image('playw.png')

        elif player_sum < banker_sum:
            self.result_label.config(text="람브 Wins!", fg="yellow")
            if self.bet_type == "banker":
                self.user_funds += self.bet_amount * 2
            self.show_winner_image('bankw.png')  
        else:
            self.result_label.config(text=" 무승부야! ", fg="black")
            self.user_funds += self.bet_amount

        self.funds_label.config(text=f"보유 코인: {self.user_funds}")

    def show_winner_image(self, image_file):
        winner_image = tk.PhotoImage(file=image_file)
        if self.winner_image_label is not None:  
            self.winner_image_label.destroy()
        self.winner_image_label = tk.Label(self.master, image=winner_image)
        self.winner_image_label.image = winner_image
        self.winner_image_label.place(x=600, y=100)

    def mainloop(self):
        self.master.mainloop()





class ham:
    import time as t 
    
    import datetime
    global w, h, sx, sy, ex, ey, makeCode, goalCode, highscore, score,runT, start_t
    # 윈도우 크기
    runT = 0
    start_t = 0
    w=900
    h=600
    # 상단 버튼 선택프레임 좌표
    sx=0            
    sy=0
    ex=130
    ey=130
    makeCode=""
    goalCode="goal"
    #점수
    highscore=0
    score=0  
    def __init__(self, window):
        self.window=window #Tk()
        self.window.title("Food Truck Game")

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.window.resizable(False, False)
        
        self.th1 = threading.Thread(target=self.get_Goal)
        # 게임 화면
        self.game_canvas=Canvas(self.window, bd=2,bg="white") 
        self.game_canvas.pack(fill="both", expand=True)
        self.set()
        # 첫 화면
        self.sgi=PhotoImage(file="img/배경1-1.png")
        self.start_canvas=Canvas(self.game_canvas,width=900,height=700,bd=0,bg="gray")
        self.game_canvas.create_window(w/2,h/2,window=self.start_canvas,tags="start_canvas")
        self.start_canvas.create_image(450,350,image=self.sgi)
        # 첫 화면 버튼
        btn_start=Button(self.start_canvas,text=" 게임 시작 ",bg="white",font=("배달의민족 주아",25),command=self.start_motion)
        btn_start.place(x=350,y=400)
        
        self.window.bind('<KeyPress>',self.key)
        self.window.mainloop()
    def get_Goal(self):
            # 여기에 get_Goal 메서드의 내용을 추가하세요.
            pass
    def makeInit(self):
        global makeCode
        makeCode = ""
        self.start()
    # 첫 시작
    def start(self):    
        global goalCode 
        self.runT = datetime.datetime.now()
        self.startT = datetime.datetime.now()
        self.goalImg=random.choice(list(self.goal.keys()))          
        self.hamburger_canvas.create_image(110,120,image=self.goalImg,tags="img")    
        goalCode=self.goal.get(self.goalImg)          
        #self.th1 = threading.Thread(target=self.get_Goal)

    # 첫 화면 올리고 카운트
    def start_motion(self):
        for x in range(10) :
            self.game_canvas.move("start_canvas",0,5)
            t.sleep(0.01)
            self.window.update()
        for x in range(35) :
            self.game_canvas.move("start_canvas",0,-30-x*20)
            t.sleep(0.01)
            self.window.update()
        self.start_canvas.destroy()
        self.countStart()

    def countStart(self):
        global makeCode
        self.scoreStr="최고점수:{0}"" 현재점수:{1}".format(str(highscore),str(score))
        self.scoreLb.config(text=self.scoreStr)

        self.countImg=[PhotoImage(file="img/3.png"),
                       PhotoImage(file="img/2.png"),
                       PhotoImage(file="img/1.png"),
                       PhotoImage(file="img/start copy.png")]
        for i in range(3): #카운트 다운
            self.hamburger_canvas.delete("all")
            tagStr="count"
            self.hamburger_canvas.create_image(-30,110,image=self.countImg[i],tags=tagStr)
            for x in range(20):
                self.hamburger_canvas.move(tagStr,7,0)
                t.sleep(0.02)
                self.window.update()
            for o in range(60):
                self.window.update()
                t.sleep(0.01)
            self.hamburger_canvas.delete("all")
        self.hamburger_canvas.create_image(100,120,image=self.countImg[3],tags=tagStr) #start!! 이미지
        for o in range(100):#start!! 이후 1초 쉬고 시작
                self.window.update()
                t.sleep(0.01)
        self.hamburger_canvas.delete("all")
        self.start()
        
    # 자료 세팅
    def set(self):

        # 버튼 이미지
        self.topPatty = PhotoImage(file = "img/버튼패티.png")
        self.topCheese = PhotoImage(file = "img/버튼치즈.png")
        self.topTomato = PhotoImage(file = "img/버튼토마토.png")
        self.topLettuce = PhotoImage(file = "img/버튼양상추.png")
        self.topUpsideBread = PhotoImage(file = "img/버튼위빵.png")
        self.topDownsideBread = PhotoImage(file = "img/버튼아래빵.png")

        # 만들기 이미지
        self.breadup=PhotoImage(file="img/위빵.png")
        self.patty=PhotoImage(file="img/패티.png")
        self.cheese=PhotoImage(file="img/치즈.png")
        self.lettuces=PhotoImage(file="img/양상추.png")
        self.downBread=PhotoImage(file="img/아래빵.png")
        self.tomatos=PhotoImage(file="img/토마토.png")
        self.dish=PhotoImage(file="img/접시.png")

        global goalCode 
        self.bgImg = PhotoImage(file ="img/배경1-2.png")
        self.game_canvas.create_image(450,300,image=self.bgImg,)

        # 버튼 프레임
        self.select_canvas=Canvas(self.game_canvas,bd=1,bg="orange")     
        self.select_canvas.place(x=90,y=20)

        # 만들기 배치
        self.make_canvas=Canvas(self.game_canvas,bd=0,width=390,height=280,bg="orange")  #메이킹 라벨
        self.make_canvas.place(x=90,y=300)
        self.makeY = 0  
        self.make(self.dish,"")


        # 버튼 배치
        self.upBreadBtn=Button(self.select_canvas,bg="red",image=self.topUpsideBread,width=100,height=100,highlightcolor="black", bd=5,command=lambda:self.click("upB"))
        self.upBreadBtn.grid(row=0,column=0,padx=10,pady=10)

        self.pattyBtn=Button(self.select_canvas,bg="orange",image=self.topPatty,width=100,height=100,bd=5,repeatdelay=1000,repeatinterval=100,command=lambda:self.click("patty"))
        self.pattyBtn.grid(row=0,column=1,padx=5,pady=5)

        self.cheeseBtn=Button(self.select_canvas,bg="gray",image=self.topCheese,width=100,height=100, bd=5,command=lambda:self.click("cheese"))
        self.cheeseBtn.grid(row=0,column=2,padx=10,pady=10)

        self.lettuceBtn=Button(self.select_canvas,bg="green",image=self.topLettuce,width=100,height=100, bd=5,command=lambda:self.click("lettuce"))
        self.lettuceBtn.grid(row=1,column=2,padx=5,pady=5)

        self.tomatoBtn=Button(self.select_canvas,bg="red",image=self.topTomato,width=100,height=100,bd=5,command=lambda:self.click("tomato"))
        self.tomatoBtn.grid(row=1,column=1,padx=10,pady=10)

        self.downBreadBtn=Button(self.select_canvas,bg="purple",image=self.topDownsideBread,width=100,height=100, bd=5,command=lambda:self.click("downB"))
        self.downBreadBtn.grid(row=1,column=0,padx=5,pady=5)
        
        # 햄버거 캔버스
        self.hamburger_canvas=Canvas(self.game_canvas,bg="black",width=220,height=210)
        self.hamburger_canvas.place(x=620,y=50)

        # scoreLb
        global score
        global highscore
        self.f= "배달의민족 주아"
        self.scoreStr="최고점수:{0}"" 현재점수:{1}".format(str(highscore),str(score))
        self.scoreLb=Label(self.game_canvas,text=self.scoreStr,font=(self.f,20,"bold"))
        self.scoreLb.place(x=610,y=280)

        # 정답 햄버거 이미지
        self.goalImg1=PhotoImage(file="img/더블치즈버거fbcbceda.png")
        self.goalImg2=PhotoImage(file="img/패티왕많이버거fbcbebdb.png")
        self.goalImg3=PhotoImage(file="img/패티치즈번갈아버거fbcbcbceda.png")
        self.goalImg4=PhotoImage(file="img/야채가좋아버거fdedecedbca.png")
        self.goalImg5=PhotoImage(file="img/토마토가좋아버거fdeeedceba.png")
        self.goalImg6=PhotoImage(file="img/양상추가좋아버거fddeddbdcdea.png")
        self.goalImg7=PhotoImage(file="img/치즈왕많이버거fcbcecdcbcdca.png")
        self.goalImg8=PhotoImage(file="img/골고루버거fcbedcdbedcbea.png")
        self.goalImg9=PhotoImage(file="img/야채는싫어버거fcbcbcbcbcba.png")
        self.goalImg10=PhotoImage(file="img/고기는싫어버거fdedecedeca.png")
        self.goalImg11=PhotoImage(file="img/혈관파괴버거fbcebcedbcea.png")
        self.goalImg12=PhotoImage(file="img/순서대로버거fedbcedbca.png")
        self.goalImg13=PhotoImage(file="img/배불러버거fbcdecda.png")

        #정답 코드
        self.goal={self.goalImg1:"fbcbceda",self.goalImg2:"fbcbebdb",self.goalImg3:"fbcbcbceda"
        ,self.goalImg4:"fdedecedbca",self.goalImg5:"fdeeedceba",self.goalImg6:"fddeddbdcdea"
        ,self.goalImg7:"fcbcecdcbcdca",self.goalImg8:"fcbedcdbedcbea",self.goalImg9:"fcbcbcbcbcba"
        ,self.goalImg10:"fdedecedeca",self.goalImg11:"fbcebcedbcea",self.goalImg12:"fedbcedbca"
        ,self.goalImg13:"fbcdecda"}

    def click(self,str):
        if str=="upB":self.make(self.breadup,"ub")
        elif str=="cheese":self.make(self.cheese,"c")
        elif str=="patty":self.make(self.patty,"p")
        elif str=="downB":self.make(self.downBread,"db")
        elif str=="lettuce":self.make(self.lettuces,"l")
        elif str=="tomato":self.make(self.tomatos,"t")

        # 재료 쌓기
    def make(self,img,code):
        global makeCode
        self.make_canvas.create_image(200 ,250-self.makeY,image=img)   
        self.makeY+=15  
        if img ==self.lettuces:
            self.makeY-=3 

        makeCode += code
        print("makeCode:",makeCode)
        if not goalCode.startswith(makeCode):
            self.endM()
        if makeCode==goalCode:
            self.endM()
    def endM(self):        
        global makeCode
        global goalCode
        print(goalCode)
        if makeCode==goalCode:
             self.runT = datetime.datetime.now()
             self.correct()
        #else: 
            #self.wrong()
        self.window.after(2000, self.endM2)
        timer = threading.Timer(2, self.endM2)
        timer.start()
        #timer.start()
        self.buttonLock()

    def endM2(self):           
        if ((self.runT-self.startT).seconds) < 60: #게임 종료 전
            self.th1 = threading.Thread(target=self.get_Goal)
            self.th1.start()
            
            self.buttonUnlock()
            #self.makeInit()

    def buttonLock(self):
        self.cheeseBtn['command']=""
        self.upBreadBtn['command']=""
        self.lettuceBtn['command']=""
        self.downBreadBtn['command']=""
        self.tomatoBtn['command']=""
        self.pattyBtn['command']=""

    def buttonUnlock(self):
        self.cheeseBtn['command']=lambda:self.click("cheese")
        self.upBreadBtn['command']=lambda:self.click("upB")
        self.lettuceBtn['command']=lambda:self.click("lettuce")
        self.downBreadBtn['command']=lambda:self.click("downB")
        self.tomatoBtn['command']=lambda:self.click("tomato")
        self.pattyBtn['command']=lambda:self.click("patty")

    def correct(self):
        global score
        global highscore
        self.corImg = PhotoImage(file="img\정답.png")
        self.make_canvas.create_image(190,140,image=self.corImg)
        score+=1
        if score>highscore :
            highscore = score
        self.scoreStr="최고점수:{0}"" 현재점수:{1}".format(str(highscore),str(score))
        self.scoreLb.config(text=self.scoreStr)

    def wrong(self):
        self.wrongImg = PhotoImage(file="img\오답.png")
        self.make_canvas.create_image(185,150,image=self.wrongImg)

    def key(self,event):
        if event.keysym == 'Left':
            self.l()
        elif event.keysym == 'Up':
            self.u()
        elif event.keysym == 'Right':
            self.r()
        elif event.keysym == 'Down':
            self.d()
    def mainloop(self):
        self.window.mainloop()
                


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("람브와 강남대학교 축제 TOUR")
        self.root.geometry("800x560")

        self.canvas = tk.Canvas(root, width=800, height=560)
        self.canvas.pack()

        self.current_screen = "opening"
        self.draw_opening_screen()

        self.character = None  # character 속성 추가

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.move_character)

    def draw_opening_screen(self):
        self.canvas.delete("all")
        opening_image = tk.PhotoImage(file="opening.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=opening_image)
        self.canvas.image = opening_image

    def draw_game_screen(self):
        self.canvas.delete("all")
        map_image = tk.PhotoImage(file="map.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=map_image)
        self.canvas.image = map_image

        # 캐릭터 이미지를 로드하고 화면에 표시
        self.character_image = tk.PhotoImage(file="cursor.png")
        self.character = self.canvas.create_image(100, 300, image=self.character_image)

        # 푸드트럭
        label1 = tk.Label(self.canvas, text="푸드트럭", bg="white")
        label1.place(x=90, y=320)
        label1.bind("<Button-1>", lambda event, label=label1: self.open_new_window_1(event, label))

        # 상담센터
        label2 = tk.Label(self.canvas, text="힐링존", bg="white")
        label2.place(x=265, y=260)
        label2.bind("<Button-1>", lambda event, label=label2: self.open_new_window_2(event, label))

        # 도서관
        label3 = tk.Label(self.canvas, text="도서관", bg="white")
        label3.place(x=500, y=160)
        label3.bind("<Button-1>", lambda event, label=label3: self.open_new_window_3(event, label))

    def handle_click(self, event):
        if self.current_screen == "opening":
            self.current_screen = "game"
            self.draw_game_screen()

    def move_character(self, event):
        x, y = event.x, event.y
        if self.character:
            self.canvas.coords(self.character, x, y)

    def open_new_window_1(self, event, label):
        new_window = tk.Toplevel(self.root)
        new_window.title("푸드트럭")
        new_window.geometry("900x700")
        label_text = "완료!"
        label.config(text=label_text)
        ham_gmae = ham(new_window)
        # 기존 창의 라벨 이름 변경
        
        ham_gmae.mainloop()

    def open_new_window_2(self, event, label):
        new_window = tk.Toplevel(self.root)
        new_window.title("상담센터")
        new_window.geometry("1400x800")
        

        baccarat_game = Baccarat(new_window)
        label_text = "완료!"
        label.config(text=label_text)
        baccarat_game.mainloop()        

        #if __name__ == "__main__":
        #    root = tk.Tk()
        #    game = Baccarat(root)
        #    game.mainloop()

        # 기존 창의 라벨 이름 변경
        
        

    def open_new_window_3(self, event, label):
        new_window = tk.Toplevel(self.root)
        new_window.title("도서관")
        new_window.geometry("1280x720")
        
        import tkinter
        import random
        import tkinter.messagebox
        import datetime

        def kdown(w):
            global key
            key = w.keysym 

        def kup(w):
            global key
            key = ""

        def mmove(w):
            global xmouse, ymouse, xpoint, ypoint
            xmouse = w.x
            ymouse = w.y
            xpoint=int(xmouse / 160)
            ypoint=int(ymouse / 72)

        def mpress(w):
            global clmouse
            clmouse = 1

        def mrelease(w):
            global clmouse
            clmouse = 0
            checkin()

        def mpoint():
            global xpoint, ypoint
            xpoint=int(xmouse / 160)
            ypoint=int(ymouse / 72)

        def ppoint():
            global ynowPaper, xnowPaper, xpaper, ypaper
            xnowPaper = wdw.coords("paper")
            ynowPaper = wdw.coords("paper")
            xpaper=int(xnowPaper / 160)
            ypaper=int(ynowPaper / 72)  

        def endZone():             
            if xmouse > 500 and xmouse < 780 and ymouse > 320 and ymouse < 500:        
                wdw.create_rectangle(500, 320, 510, 500, fill="yellow", width=0, tag="getZone")
                wdw.create_rectangle(500, 318, 790, 330, fill="yellow", width=0, tag="getZone")
                wdw.create_rectangle(780, 320, 790, 500, fill="yellow", width=0, tag="getZone")
                wdw.create_rectangle(500, 488, 790, 500, fill="yellow", width=0, tag="getZone")
            else:
                wdw.delete("getZone")   
            moniter.after(100, endZone)

        def moving(): 
            global count, xonAir, yonAir, Npage, x, y, nx, ny
            global Npaper, now
            wdw.delete("print")
            if key == 'k':
                fnt = ("Times New Roman", 40, "bold")
                wdw.create_text(650, 100, text="현재 모은 페이지\n", fill="black", font=fnt, tag="print")
                wdw.create_text(650, 200, text=str(end)+' p', fill="black", font=fnt, tag="print")  
                wdw.create_text(200, 100, text="최고 점수! 현재... "+str(cscore)+" 점!", fill="yellow", font=("Times New Roman", 30, "bold"), tag="print")  
            if Npaper == 0:
                xlist = [128, 256, 384, 412, 896, 1024, 1152, 1280]
                ylist = [72, 720]
                xonAir = random.choice(xlist)   
                yonAir = random.choice(ylist)
                Npage = random.choice(page)
                if xonAir < 640 :
                    if yonAir > 360:
                        wdw.create_image(xonAir, yonAir, image = LUpaper, tag = "paper")
                    wdw.create_image(xonAir, yonAir, image = LDpaper, tag = "paper") 
                if yonAir > 360:
                    wdw.create_image(xonAir, yonAir, image = RUpaper, tag = "paper")
                wdw.create_image(xonAir, yonAir, image = RDpaper, tag = "paper")
                Npaper = 1  
                x, y = wdw.coords("paper")[:2]
                nx = int(x/160)
                ny = int(y/72)     
            if now == 0:
                if xonAir < 640 :
                    if yonAir > 360:
                        wdw.move("paper", mov, -mov)
                        if ny < 0 or ny > 10:
                            count = 1
                    else:  
                        wdw.move("paper", mov, mov)
                        if ny < 0 or ny > 10:
                            count = 1
                else:
                    if yonAir > 360:
                        wdw.move("paper", -mov, -mov)
                        if ny < 0 or ny > 10:
                            count = 1
                    else:
                        wdw.move("paper", -mov, mov)
                        if ny < 0 or ny > 10:
                            count = 1
            x, y = wdw.coords("paper")[:2]
            nx = int(x/160)
            ny = int(y/72) 
            if count == 1:
                    wdw.delete("paper")
                    count = 0  
                    Npaper = 0
            if xpoint == nx and ypoint == ny:
                now = 1
                wdw.delete("paper")
                wdw.create_image(x, y, image = Npage, tag = "paper")
                if clmouse == 1:    
                    movein()                          
            if now == 1 and not(xpoint == nx and ypoint == ny):
                wdw.delete("paper")
                xypaper() 
                now = 0   
            moniter.after(20, moving)    

        def movein():
                if clmouse == 1:
                    wdw.delete("paper")
                    if xonAir < 640 :
                        if yonAir > 360:
                            wdw.create_image(xmouse, ymouse, image = LUpaper, tag = "paper")
                        wdw.create_image(xmouse, ymouse, image = LDpaper, tag = "paper") 
                    if yonAir > 360:
                        wdw.create_image(xmouse, ymouse, image = RUpaper, tag = "paper")
                    wdw.create_image(xmouse, ymouse, image = RDpaper, tag = "paper")
                    moniter.after(20, movein) 

        def xypaper():
            if xonAir < 640 :
                if yonAir > 360:
                    wdw.create_image(x, y, image = LUpaper, tag = "paper")
                wdw.create_image(x, y, image = LDpaper, tag = "paper") 
            if yonAir > 360:
                wdw.create_image(x, y, image = RUpaper, tag = "paper")
            wdw.create_image(x, y, image = RDpaper, tag = "paper") 

        def checkin():
            global end, Npaper, start_t, score, cscore
            if clmouse == 0 and (xmouse > 500 and xmouse < 780 and ymouse > 320 and ymouse < 500) and (x > 500 and x < 780 and y > 320 and y < 500): 
                wdw.delete("paper")
                if Npage == page[0] and '1' not in end:        
                    end.insert(0, '1')
                elif Npage == page[1] and '2' not in end:
                    end.insert(1, '2')
                elif Npage == page[2] and '3' not in end:
                    end.insert(2, '3')
                elif Npage == page[3] and '4' not in end:
                    end.insert(3, '4')    
                elif Npage == page[4] and '5' not in end:
                    end.insert(4, '5')
                elif Npage == page[5] and '6' not in end:
                    end.insert(5, '6')
                elif Npage == page[6] and '7' not in end:
                    end.insert(6, '7')           
                elif Npage == page[7]:
                    end = []         
                Npaper = 0
                if '1' in end and '2' in end and '3' in end and '4' in end and '5' in end and '6' in end and '7' in end:
                    end_t = datetime.datetime.now()
                    tkinter.messagebox.showinfo("전부 모았어!\n", (str((end_t - start_t).seconds) + "초 걸렸어!"))
                    end = []
                    score = 150 - int((end_t-start_t).seconds)
                    if score < 0:
                        score = 0
                    if score >= cscore:
                        cscore = score
                        last = tkinter.messagebox.askyesno(str(cscore) + " 점 획득!", "그만 할까?")
                    else:   
                        last = tkinter.messagebox.askyesno(str(score) + " 점 획득!", "그만 할까?")    
                    if last == True:
                        moniter.destroy()
                    start_t = datetime.datetime.now()    

        def win3(window):
            global moniter, wdw, page, LDpaper, LUpaper, RDpaper, RUpaper, start_t, lib, key, xmouse, ymouse, clmouse, count, xpoint, ypoint, lon, score, end, cscore, Npaper, now, mov
            key = ""
            xmouse = 0
            ymouse = 0
            clmouse = 0
            count = 0
            xpoint = 0
            ypoint = 0
            lon = 0
            score = 0
            end = []
            cscore = 0
            score = 0
            Npaper = 0
            now = 0
            mov = 10
            moniter = window
            moniter.bind("<Motion>", mmove)  
            moniter.bind("<ButtonPress>", mpress)    
            moniter.bind("<ButtonRelease>", mrelease)
            moniter.bind("<KeyPress>", kdown)
            moniter.bind("<KeyRelease>", kup)
            wdw = tkinter.Canvas(moniter, width=1290, height=720, bg="white")
            moniter.title("The Secret of KN Library")
            moniter.resizable(width=False, height=False)
            wdw.pack()
            lib = tkinter.PhotoImage(file="p\\ilb.png")
            wdw.create_image(640, 360, image=lib, tag="map")
            def EX():
                global lon
                lon+=1
                if lon == 1:    
                    text.insert(tkinter.END, "지금부터 게임을 설명할게!\n\n") 
                    text.insert(tkinter.END, "얼마 전, 못된 관람객들이 도서관 책들의 페이지를 찢어버렸어...\n\n")
                if lon == 2:
                    text.delete("1.0", "end")
                    text.insert(tkinter.END, "지금부터 잃어버린 페이지를 되찾는 거야!\n\n")
                if lon == 3:
                    text.delete("1.0", "end")
                    text.insert(tkinter.END, "마우스를 날아다니는 종이에 가져다 놓으면 몇 페이지인지를 확인할 수 있어!\n\n")
                if lon == 4:
                    text.delete("1.0", "end")
                    text.insert(tkinter.END, "종이에 마우스를 얹고, 클릭한 채로 움직여봐!\n\n")
                if lon == 5:
                    text.delete("1.0", "end")
                    text.insert(tkinter.END, "그러다 보면 책의 노란 선이 나타날 거야. 거기서 마우스를 놓으면...\n\n참고로 '꽝'은 조심하는 게 좋아! 뭐, 겪어보면 알겠지만!\n\n")
                if lon == 6:
                    text.delete("1.0", "end")
                    text.insert(tkinter.END, "모은 페이지는 k 키를 눌러 확인할 수 있어!\n\n")
                if lon == 7:
                    text.delete("1.0", "end")
                    text.insert(tkinter.END, "그럼 시작한다?")
                if lon == 8:    
                    bt.destroy()
                    bt2.destroy()
                    text.destroy()
            def EX2():
                global lon
                if lon > 1:
                    lon-=1
                    if lon == 1:    
                        text.delete("1.0", "end")
                        text.insert(tkinter.END, "지금부터 게임을 설명할게!\n\n") 
                        text.insert(tkinter.END, "얼마 전, 못된 관람객들이 도서관 책들의 페이지를 찢어버렸어...\n\n")
                    if lon == 2:
                        text.delete("1.0", "end")
                        text.insert(tkinter.END, "지금부터 잃어버린 페이지를 되찾는 거야!\n\n")
                    if lon == 3:
                        text.delete("1.0", "end")
                        text.insert(tkinter.END, "마우스를 날아다니는 종이에 가져다 놓으면 몇 페이지인지를 확인할 수 있어!\n\n")
                    if lon == 4:
                        text.delete("1.0", "end")
                        text.insert(tkinter.END, "종이에 마우스를 얹고, 클릭한 채로 움직여봐!\n\n")
                    if lon == 5:
                        text.delete("1.0", "end")
                        text.insert(tkinter.END, "그러다 보면 책의 노란 선이 나타날 거야. 거기서 마우스를 놓으면...\n\n참고로 '꽝'은 조심하는 게 좋아! 뭐, 겪어보면 알겠지만!\n\n")
                    if lon == 6:
                        text.delete("1.0", "end")
                        text.insert(tkinter.END, "모은 페이지는 k 키를 눌러 확인할 수 있어!\n\n")
                    if lon == 7:
                        text.delete("1.0", "end")
                        text.insert(tkinter.END, "그럼 시작한다?") 
            bt = tkinter.Button(new_window, text="다음", font = ("Times New Roman", 30, "bold"), command=EX)
            bt2 = tkinter.Button(new_window, text="이전", font = ("Times New Roman", 30, "bold"), command=EX2)
            text=tkinter.Text(new_window, font = ("Times New Roman",30), bg = "gray")
            text.place(x = 250, y = 2, width= 800, height= 260)
            bt.place(x = 750, y = 250, width=300, height=100)
            bt2.place(x = 250, y = 250, width=300, height=100)
            LDpaper = tkinter.PhotoImage(file="p\\LDpaper.png")
            LUpaper = tkinter.PhotoImage(file="p\\LUpaper.png")
            RDpaper = tkinter.PhotoImage(file="p\\RDpaper.png")
            RUpaper = tkinter.PhotoImage(file="p\\RUpaper.png")
            page = [
                tkinter.PhotoImage(file="p1.png"),
                tkinter.PhotoImage(file="p2.png"),
                tkinter.PhotoImage(file="p3.png"),
                tkinter.PhotoImage(file="p4.png"),
                tkinter.PhotoImage(file="p5.png"),
                tkinter.PhotoImage(file="p6.png"),
                tkinter.PhotoImage(file="p7.png"),
                tkinter.PhotoImage(file="p0.png")
            ]
            start_t = datetime.datetime.now()
            endZone()
            moving()

        win3(new_window)
        # 기존 창의 라벨 이름 변경
        label_text = "완료!"
        label.config(text=label_text)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()


