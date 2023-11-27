from ursina import*;from random import*;from rigid import*
app=Ursina(development_mode=False)
world = BulletWorld()
world.setGravity(Vec3(0, -18, 0))
class gameoveri(Entity):
    def __init__(self,**kwargs):super().__init__(model="cube",collider="box",visible=False, **kwargs)
class Mape(Entity):
    def __init__(self,**kwargs):super().__init__(model="cube",collider="box",color=color.rgb(255,228,117),eternal=True, **kwargs);RigidBody(world=world, shape=BoxShape(), entity=self)
ground,leftwall,rightwall=Mape( scale=(11,1,1)),Mape( scale=(1,10.1,1),x=-5,y=5.5),Mape(scale=(1,10.1,1),x=5,y=5.5)        
class fruits(Entity):
    def __init__(self,typ ,**kwargs):    
        self.typ=typ
        super().__init__(model="quad",collider="sphere",texture="assets/fu"+str(self.typ),scale=(self.typ+1)*0.5, **kwargs)  
        self.havehit=False
        self.colli=RigidBody(world=world, shape=SphereShape(),entity=self, mass=(self.typ+1)*2)
    def update(self):
        global gamegeror
        if gamegeror.isover:
            if self.y<-40 :
                self.colli.remove()
                return destroy(self)
        else:
            try:
                self.colli.z=0
            except:
                pass
        self.world_rotation_x=0
        self.world_rotation_y=0
        ent=self.intersects()
        for hitinfo in ent.entities:
            if str(hitinfo.name)=="fruits":
                self.havehit=True
                if hitinfo.typ==self.typ:     
                    gamegeror.score+=(self.typ+1)
                    try:
                        posx=self.world_x+hitinfo.world_x
                        posy=self.world_y+hitinfo.world_y
                        fruits(position=(posx*0.5,posy*0.5,0),typ=self.typ+1)
                    except:       
                        fruits(position=(0,(self.typ+1)*0.5,0),typ=self.typ+1)
                    hitinfo.colli.remove()
                    self.colli.remove()
                    self.havehit=True
                    destroy(hitinfo)
                    return destroy(self)
            elif str(hitinfo.name)=="mape":
                self.havehit=True
            elif str(hitinfo.name)=="gameoveri" and self.havehit:
                gamegeror.gameover()
                return destroy(self)          
def update():world.doPhysics(time.dt)
class GameGeror(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.scoretext=Text(parent=self,text="score:0",scale=3,position=(-0.8,0.4,0),color=color.black)
        self.score=0
        self.isover=False
        self.playbut=Entity(model="quad",collider="box",parent=self,scale=(0.4,0.2,1),texture="assets/playbut")
        self.player=Player(position=(0,12,0),enabled=False,texture="assets/player",scale=2)
        self.fontof=Entity(model="quad",scale=(40,40,1),y=10,z=5,color=color.cyan)
    def setmenu(self):self.playbut.enabled=True;self.player.enabled=False
    def setgame(self):self.isover=False;self.playbut.enabled=False;self.player.enabled=True;self.score=0;self.player.x=0
    def update(self):
        self.player.nexteur.enabled=self.player.enabled
        if self.playbut.visible and self.playbut.hovered and held_keys["left mouse"]:self.setgame()
        self.scoretext.text="score:"+str(self.score)
    def gameover(self):
        self.isover=True
        for ele in scene.children:
            if str(ele.name)=="fruits" and hasattr(ele,"colli"):ele.colli.remove();destroy(ele)
        self.setmenu()
class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(model="quad", **kwargs)
        self.timer=0
        self.actualfu=randint(0,5)
        self.nextfu=randint(0,5)
        self.actualeur=Entity(model="quad",parent=self,scale=0.5,position=(0,0,-2),texture="assets/fu"+str(self.actualfu))
        self.nexteur=Entity(model="quad",parent=camera.ui,scale=0.2,position=(0.4,0.3,0),texture="assets/fu"+str(self.nextfu))
    def input(self,key):
        if key=="space" and self.timer<0:
            self.timer=1
            fruits(position=self.position,typ=self.actualfu)
            self.actualfu=self.nextfu
            self.nextfu=randint(0,5)
            self.actualeur.texture="assets/fu"+str(self.actualfu)
            self.nexteur.texture="assets/fu"+str(self.nextfu)
    def update(self):
        self.timer-=time.dt
        self.x+=(held_keys["right arrow"]-held_keys["left arrow"])*time.dt*10
        dist=(4,4,3.75,3.25,3.25,3)[self.actualfu]
        if self.x>dist:self.x=dist
        if self.x<-dist:self.x=-dist
gameoveri(position=(0,11,0),scale=(10,1,1))
gamegeror=GameGeror()
camera.fov=15
camera.y=7
camera.orthographic=True
app.run()