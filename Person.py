from Types import PersonState, Quarantine
import random
from utils import *

p = 0.1


class Person:
    age = 0
    age_group = 0
    background_sickness = 0
    exposure = 0  # How active one person is
    follow_protocol = 0
    quarantine = 0
    state = PersonState.EMPTY
    state_count = 0
    gender = 0
    exposure_ratio = 0
    vulnerability_ratio = 0 
    death_ratio = 0
    incubation_period = 0  # 2-14 (3-5 har mye vekt)
    bmi = 0
    smoking = 0

    def __init__(self):
        pass

    def generate_random_values(self):
        self.age = self.set_age()
        self.age_group = get_age_group(self.age)
        self.background_sickness = get_background_sickness(self.age)
        self.exposure = random.randint(1, 3)

        # TODO: increase follow_protocol depending on age
        self.follow_protocol = random.uniform(0, 1)
        self.quarantine = 0
        self.gender = Gender.FEMALE if random.random() < 0.5 else Gender.MALE

        chance_of_inf = p
        # self.state = states[1] if random.uniform(0, 1) < chance_of_inf else states[0]
        self.state = PersonState.INFECTIOUS if random.uniform(0, 1) < chance_of_inf else PersonState.HEALTHY
        self.state_count = 0

    def get_vulnerability_ratio(self):
        #risk of getting infection
        
        pass

    def get_risk_ratio(self, mask, distancing, hygiene, curfew):
        # risk of infecting others
        if self.person_state not in [PersonState.SICK, PersonState.INFECTIOUS]:
            return 0
        else:
            if self.quarantine == Quarantine.TOTAL_ISOLATION:
                # any chance of people breaking isolation?
                # what about people you live with? are they also isolated, or quarantined
                # in those cases they can be infected...
                return 0 
            
            # TODO or Not TODO? That is the question
            
            elif self.quarantine == Quarantine.QUARANTINE:
            # how strict is the quarantine (can you go to stores, be with others)
            # how strictly do you follow protocols?
                #if(self.follow_protocol == )
         
        #if infected or sick but not in quarantine or isolation
        else: 
            protocols = (distancing + mask + hygiene)/3
            # social distancing rules =
            # face mask rules / recommendations
            # + distancing (i.e one meter rule)    
            # + hygiene rules 
            
            risk_ratio = protocols * self.follow_protocol
            risk ratio = risk_ratio * self.exposure
            # following protocols * social distancing rules
            # + exposure??
            # + staying at home rules (i.e portforbud) (can be part of the exposure variable??)
            return risk_ratio
            

        pass
    
    def get_death_ratio(self):
        # background_sickness, maybe age, lifestyle (smoking, weight), health care (respirator, medicines)
        # https://www.fhi.no/contentassets/8a971e7b0a3c4a06bdbf381ab52e6157/vedlegg/andre-halvar-2020/2020.09.23-ukerapport-uke-38-covid-19.pdf
        # page 24
        pass
    
    def print_self(self):
        print('Age =', self.age)
        print('bs =', self.background_sickness)
        print('Exposure =', self.exposure)
        print('Follow protocol =', self.follow_protocol)
        print('In quarantine =', self.quarantine)
        print('State =', self.state)
