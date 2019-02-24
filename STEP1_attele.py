"""
on récupère les rapports placés en plus

"""




##imports 

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException   
import numpy as np
import pandas as pd

##constants
number_of_days=[31,28,31,30,31,30,31,31,30,31,30,31]

year=2018
month_initial=9
day_initial=10

month_final=12
day_final=31


l_trot_initial=0
l_plat_initial=0

##functions

#UPDATE: retrieve information from plat kind of race
def retrieve_race_information_plat(l):

    xpath_infos_course="//ul[contains(@class,'course-infos-header-extras-main')]"
    infos_course=driver.find_element_by_xpath(xpath_infos_course).text
    
    if(infos_course.split('\n')[0]!="Plat"):
        return(l)

    BDD_plat[l,3]=infos_course


    
    xpath_piste="//li[contains(@class,'bandeau-nav-content-scroll-item--current')]//div[contains(@class,'reunion-hippodrome')]"
    piste=driver.find_element_by_xpath(xpath_piste).text
    BDD_plat[l,0]=piste

    
    xpath_time="//li[contains(@class,'bandeau-nav-content-scroll-item--current')]//span[contains(@class,'statut-course')]"
    times=driver.find_element_by_xpath(xpath_time).text.split('.')
    hour=times[1]
    day=times[0]
    BDD_plat[l,1]=hour
    BDD_plat[l,2]=day

    
    xpath_infos_conditions="//div[contains(@class,'course-infos-conditions')]"
    infos_conditions=driver.find_element_by_xpath(xpath_infos_conditions).text
    BDD_plat[l,4]=infos_conditions


    xpath_infos_meteo="//div[contains(@class,'course-infos-meteo')]"
    infos_meteo=driver.find_element_by_xpath(xpath_infos_meteo).text
    BDD_plat[l,5]=infos_meteo


    xpath_infos_meteo_icon="//div[contains(@class,'course-infos-meteo')]//span"
    meteo_icon=driver.find_element_by_xpath(xpath_infos_meteo_icon)
    meteo_icon=meteo_icon.get_attribute("class")
    BDD_plat[l,6]=meteo_icon

    try:
        driver.execute_script("window.scrollTo(0, 800)") 
        xpath_partants="//li[contains(@class,'partants')]"
        element=driver.find_element_by_xpath(xpath_partants)
        element.click()
        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
        tbody_partants=driver.find_elements_by_xpath(xpath_tbody)
        n=len(tbody_partants)
        for i in range(n):
            BDD_plat[l+i,7]=tbody_partants[i].text
            for j in range(7):
                BDD_plat[l+i,j]=BDD_plat[l,j]


        xpath_details="//div[contains(@class,'participants-details')]"
        details=driver.find_elements_by_xpath(xpath_details)
        n=len(details)
        for i in range(n):
            suppl_oeillere=[]
            try :
                suppl=details[i].text
                suppl_oeillere.append(suppl)
            except:
                suppl_oeiller.append(False)
            try:
                xpath_oeillere=".//*[local-name() = 'use']"
                oeillere=details[i].find_element_by_xpath(xpath_oeillere).get_attribute("xlink:href")
                suppl_oeillere.append(oeillere)
            except:
                suppl_oeillere.append(False)
            BDD_plat[l+i,8]=suppl_oeillere
        
        
        try:
            xpath_arrivee="//div[contains(@class,'participants-nav-region')]//li[contains(@class,'arrivee')]"
            element=driver.find_element_by_xpath(xpath_arrivee)
            element.click()
        except:
            l=l
        
    
        xpath_option="//select[@id='participantsSelect']//option[text()='Numéro']"
        driver.find_element_by_xpath(xpath_option).click()
        time.sleep(2)
        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
        tbody_arrivee=driver.find_elements_by_xpath(xpath_tbody)
        n=len(tbody_arrivee)
        for i in range(n):
            BDD_plat[l+i,9]=tbody_arrivee[i].text
    
    
    
        driver.execute_script("window.scrollTo(0,0)") 
        return(l+n)



    except:
        driver.refresh()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 800)") 
        xpath_partants="//li[contains(@class,'partants')]"
        element=driver.find_element_by_xpath(xpath_partants)
        element.click()
        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
        tbody_partants=driver.find_elements_by_xpath(xpath_tbody)
        n=len(tbody_partants)
        for i in range(n):
            BDD_plat[l+i,7]=tbody_partants[i].text
            for j in range(7):
                BDD_plat[l+i,j]=BDD_plat[l,j]


        xpath_details="//div[contains(@class,'participants-details')]"
        details=driver.find_elements_by_xpath(xpath_details)
        n=len(details)
        for i in range(n):
            suppl_oeillere=[]
            try :
                suppl=details[i].text
                suppl_oeillere.append(suppl)
            except:
                suppl_oeiller.append(False)
            try:
                xpath_oeillere=".//*[local-name() = 'use']"
                oeillere=details[i].find_element_by_xpath(xpath_oeillere).get_attribute("xlink:href")
                suppl_oeillere.append(oeillere)
            except:
                suppl_oeillere.append(False)
            BDD_plat[l+i,8]=suppl_oeillere
        
        
        try:
            xpath_arrivee="//div[contains(@class,'participants-nav-region')]//li[contains(@class,'arrivee')]"
            element=driver.find_element_by_xpath(xpath_arrivee)
            element.click()
        except:
            l=l
        
    
        xpath_option="//select[@id='participantsSelect']//option[text()='Numéro']"
        driver.find_element_by_xpath(xpath_option).click()
        time.sleep(2)
        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
        tbody_arrivee=driver.find_elements_by_xpath(xpath_tbody)
        n=len(tbody_arrivee)
        for i in range(n):
            BDD_plat[l+i,9]=tbody_arrivee[i].text
    
    
    
        driver.execute_script("window.scrollTo(0,0)") 
        return(l+n)




#retrieve information from a race
def retrieve_race_information(l_trot,l_plat):
    


    xpath_infos_course="//ul[contains(@class,'course-infos-header-extras-main')]"
    infos_course=driver.find_element_by_xpath(xpath_infos_course).text

    if(infos_course.split(' ')[0]!=("Trot")):

        try:
            #l_plat=retrieve_race_information_plat(l_plat)
            return(l_trot,l_plat,True)
        except:
            return(l_trot,l_plat,True)
    l=l_trot
    BDD_trot[l,3]=infos_course
    
    try:
        xpath_piste="//li[contains(@class,'bandeau-nav-content-scroll-item--current')]//div[contains(@class,'reunion-hippodrome')]"
        piste=driver.find_element_by_xpath(xpath_piste).text
        BDD_trot[l,0]=piste
    except:
        print("piste_exception")
    
    try:
        xpath_time="//li[contains(@class,'bandeau-nav-content-scroll-item--current')]//span[contains(@class,'statut-course')]"
        times=driver.find_element_by_xpath(xpath_time).text.split('.')
    
        hour=times[1]
        day=times[0]
        BDD_trot[l,1]=hour
        BDD_trot[l,2]=day
    except:
        print("times exception")
    
    try:
        xpath_infos_conditions="//div[contains(@class,'course-infos-conditions')]"
        infos_conditions=driver.find_element_by_xpath(xpath_infos_conditions).text
        BDD_trot[l,4]=infos_conditions
    except:
        print("info_conditions exception")

    try:
        xpath_infos_meteo="//div[contains(@class,'course-infos-meteo')]"
        infos_meteo=driver.find_element_by_xpath(xpath_infos_meteo).text
        BDD_trot[l,5]=infos_meteo
    except:
        print("meteo exception")
    
    try:
        xpath_infos_meteo_icon="//div[contains(@class,'course-infos-meteo')]//span"
        meteo_icon=driver.find_element_by_xpath(xpath_infos_meteo_icon)
        meteo_icon=meteo_icon.get_attribute("class")
        BDD_trot[l,6]=meteo_icon
    except:
        print("meteo_icon exception")

    try:

        driver.execute_script("window.scrollTo(0, 800)") 
        xpath_partants="//li[contains(@class,'partants')]"
        element=driver.find_element_by_xpath(xpath_partants)
        element.click()
        time.sleep(2)

        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
    
        tbody_partants=driver.find_elements_by_xpath(xpath_tbody)

        n=len(tbody_partants)

        for i in range(n):
            BDD_trot[l+i,7]=tbody_partants[i].text
            for j in range(7):
                BDD_trot[l+i,j]=BDD_trot[l,j]
                
        xpath_details="//div[contains(@class,'participants-details')]"
        details=driver.find_elements_by_xpath(xpath_details)

        n=len(details)

        for i in range(n):
            try :
                xpath_fer=".//*[local-name() = 'svg']"
                fer=details[i].find_element_by_xpath(xpath_fer).get_attribute("class")
                BDD_trot[l+i,8]=fer
    
            except:
                BDD_trot[l+i,8]=False
    
    
            
        try:
            xpath_arrivee="//div[contains(@class,'participants-nav-region')]//li[contains(@class,'arrivee')]"
            element=driver.find_element_by_xpath(xpath_arrivee)
            element.click()
        except:
            l=l
        
        xpath_option="//select[@id='participantsSelect']//option[text()='Numéro']"
        driver.find_element_by_xpath(xpath_option).click()
        time.sleep(2)
        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
        tbody_arrivee=driver.find_elements_by_xpath(xpath_tbody)

        n=len(tbody_arrivee)

        for i in range(n):
            BDD_trot[l+i,9]=tbody_arrivee[i].text
    
    
        driver.execute_script("window.scrollTo(0,600)")
        

    

        return(l+n,l_plat,False)
        
        
    
    except:

        driver.refresh()
        time.sleep(3)


        driver.execute_script("window.scrollTo(0, 800)") 
        xpath_partants="//li[contains(@class,'partants')]"
        element=driver.find_element_by_xpath(xpath_partants)
        element.click()
        time.sleep(1)

        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
    
        tbody_partants=driver.find_elements_by_xpath(xpath_tbody)

        n=len(tbody_partants)
        for i in range(n):
            BDD_trot[l+i,7]=tbody_partants[i].text
            for j in range(7):
                BDD_trot[l+i,j]=BDD_trot[l,j]
                
        xpath_details="//div[contains(@class,'participants-details')]"
        details=driver.find_elements_by_xpath(xpath_details)

        n=len(details)

        for i in range(n):
            try :
                xpath_fer=".//*[local-name() = 'svg']"
                fer=details[i].find_element_by_xpath(xpath_fer).get_attribute("class")
                BDD_trot[l+i,8]=fer
    
            except:
                BDD_trot[l+i,8]=False
    
    
            
        try:
            xpath_arrivee="//div[contains(@class,'participants-nav-region')]//li[contains(@class,'arrivee')]"
            element=driver.find_element_by_xpath(xpath_arrivee)
            element.click()
        except:
            l=l
        
        xpath_option="//select[@id='participantsSelect']//option[text()='Numéro']"
        driver.find_element_by_xpath(xpath_option).click()
        time.sleep(1)
        xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
        tbody_arrivee=driver.find_elements_by_xpath(xpath_tbody)

        n=len(tbody_arrivee)

        for i in range(n):
            BDD_trot[l+i,9]=tbody_arrivee[i].text
    
    
        driver.execute_script("window.scrollTo(0,0)")

        return(l+n,l_plat,False)
    
    




#retrieve one day of one reunion
def retrieve_reunion_information(j,l_trot,l_plat):

    driver.execute_script("window.scrollTo(0, 0)")

    time.sleep(3)

    xpath_place="//div[@class='bandeau-course-region']"
    elements=driver.find_element_by_xpath(xpath_place)

    number_of_races=len(elements.text.split('C'))-1
    
    xpath_race_number="//p[@class='bandeau-nav-content-scroll-item-numero']"
    element=driver.find_element_by_xpath(xpath_race_number)
    try:
        first=int(element.text[-1])
    except:
        first=1
        print("first=1")
    
    try:
        l_trot,l_plat,galop=retrieve_race_information(l_trot,l_plat)
        if(galop):
            number_of_races=0

    except BaseException as e :
        print("exception",str(e))

    for i in range(1,number_of_races):
        driver.execute_script("window.scrollTo(0, 0)")
        try:
            xpath_race="//li[contains(@class,'ARRIVEE')][@data-numordre='"+str(i+first)+"']"
            driver.find_element_by_xpath(xpath_race).click()
            time.sleep(2)
            l_trot,l_plat,galop=retrieve_race_information(l_trot,l_plat)

        except BaseException as e :
            print("exception",str(e))
    driver.execute_script("window.scrollTo(0, 0)") 
    xpath="//div[@class='bandeau-nav-content-scroll-item-numero']//span[contains(text(),'R"+str(j+1)+"')]"
    driver.find_element_by_xpath(xpath).click()
    return(True,l_trot,l_plat)



#retrieve information of one day
def retrieve_day_information(l_trot,l_plat):
    
    place_exists=True    
    j=1

    while(place_exists):
        try:
            print("REUNION ",j)
            place_exists,l_trot,l_plat=retrieve_reunion_information(j,l_trot,l_plat)
        except:
            place_exists,l_trot,l_plat=False,l_trot,l_plat
            print("error when trying to retrieve reunion ",j)
        j+=1
    print("number of trot samples :",l_trot,"number of plat samples :",l_plat)
    return(l_trot,l_plat)    

#retrieve information from day1 and day2 of the same month
def retrieve_period_information(year,month,day1,day2,l_trot,l_plat):
    for day in range(day1,day2):
        print("month",month,"day",day)
        if(month<10):
            str_month='0'+str(month)
        else:
            str_month=str(month)
        if(day<10):
            str_day='0'+str(day)
        else:
            str_day=str(day)
        driver.get('https://www.pmu.fr/turf/'+str_day+str_month+str(year)+'/R1/C1')
        time.sleep(3)
        try:
            l_trot,l_plat=retrieve_day_information(l_trot,l_plat)
        except:
            l_trot,l_plat=l_trot,l_plat
            print("error when trying to retrieve day ",month,day)
    return(l_trot,l_plat)
            
   
#retrieve information from day_initial to day_final
def retrieve_information():
    l_trot=l_trot_initial
    l_plat=l_plat_initial
    if(month_initial==month_final):
        month=month_initial
        try:
            l_trot,l_plat=retrieve_period_information(year,month,day_initial,day_final,l_trot,l_plat)
        except:
            print("error when trying to retrieve period_information")
   
    else:
        month=month_initial
        try:
            l_trot,l_plat=retrieve_period_information(year,month,day_initial,number_of_days[month],l_trot,l_plat)
        except:
            print("error when trying to retrieve period_information")
   
    
        for month in range(month_initial+1,month_final):
            try:
                l_trot,l_plat=retrieve_period_information(year,month,1,number_of_days[month],l_trot,l_plat)
            except:
                print("error when trying to retrieve period_information")
   
        month=month_final
        try:
            l_trot,l_plat=retrieve_period_information(year,month,1,day_final,l_trot,l_plat)
        except:
            print("error when trying to retrieve period_information")
   
    
    
##retrieve information from pmu website and store it into a numpy array

BDD_aux_trot = np.zeros((1000000,11))
BDD_trot = np.array(BDD_aux_trot,dtype=object)

BDD_aux_plat = np.zeros((1000000,11))
BDD_plat = np.array(BDD_aux_plat,dtype=object)

driver = webdriver.Chrome("C:/Users/Clément/Desktop/chromedriver.exe")            
retrieve_information()
driver.quit()

##remove all the zeros

n,l2=BDD_trot.shape
i=n-1
while(i>=0 and BDD_trot[i,1]==0):
    i+=(-1)

BDD_trot=BDD_trot[:i+1,:]
      
n,l2=BDD_plat.shape
i=n-1
while(i>=0 and BDD_plat[i,1]==0):
    i+=(-1)

BDD_plat=BDD_plat[:i+1,:]
          




## Save the BDD to csv format
 
import pandas as pd 

df_trot=pd.DataFrame(BDD_trot,columns=["piste","hour","day","infos-course","infos-conditions","infos_meteo","meteo_icon","infos_partants","fer","infos_arrivee","rapports"])
df_trot.to_csv('BDD_trot_'+str(year)+'_'+str(day_initial)+'_'+str(month_initial)+'_'+str(day_final)+'_'+str(month_final)+'.csv')

df_plat=pd.DataFrame(BDD_plat,columns=["piste","hour","day","infos-course","infos-conditions","infos_meteo","meteo_icon","infos_partants","oeillere_suppl","infos_arrivee","rapports"])
df_plat.to_csv('BDD_plat_'+str(year)+'_'+str(day_initial)+'_'+str(month_initial)+'_'+str(day_final)+'_'+str(month_final)+'.csv')




