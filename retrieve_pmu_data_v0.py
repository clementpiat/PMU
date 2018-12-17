##imports 

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException   
import numpy as np

##constants

year=2018

##functions

def retrieve_race_information(l):
    print(l)


    xpath_infos_course="//ul[contains(@class,'course-infos-header-extras-main')]"
    infos_course=driver.find_element_by_xpath(xpath_infos_course).text
    if(infos_course.split(' ')[0]!="Trot"):
        return(l)
    BDD[l,3]=infos_course

    
    xpath_piste="//li[contains(@class,'bandeau-nav-content-scroll-item--current')]//div[contains(@class,'reunion-hippodrome')]"
    piste=driver.find_element_by_xpath(xpath_piste).text
    BDD[l,0]=piste
    
    #xpath_time="//div[contains(@class,'header-dock-clock')]"
    xpath_time="//li[contains(@class,'bandeau-nav-content-scroll-item--current')]//span[contains(@class,'statut-course')]"
    times=driver.find_element_by_xpath(xpath_time).text.split('.')
    hour=times[1]
    day=times[0]
    BDD[l,1]=hour
    BDD[l,2]=day
    
    
    xpath_infos_conditions="//div[contains(@class,'course-infos-conditions')]"
    infos_conditions=driver.find_element_by_xpath(xpath_infos_conditions).text
    BDD[l,4]=infos_conditions

    
    xpath_infos_meteo="//div[contains(@class,'course-infos-meteo')]"
    infos_meteo=driver.find_element_by_xpath(xpath_infos_meteo).text
    BDD[l,5]=infos_meteo

    
    xpath_infos_meteo_icon="//div[contains(@class,'course-infos-meteo')]//span"
    meteo_icon=driver.find_element_by_xpath(xpath_infos_meteo_icon)
    meteo_icon=meteo_icon.get_attribute("class")
    BDD[l,6]=meteo_icon
    
    driver.execute_script("window.scrollTo(0, 700)") 
    time.sleep(1)
    xpath_partants="//li[contains(@class,'partants')]"
    element=driver.find_element_by_xpath(xpath_partants)
    element.click()

    xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
    tbody_partants=driver.find_elements_by_xpath(xpath_tbody)
    n=len(tbody_partants)
    for i in range(n):
        BDD[l+i,7]=tbody_partants[i].text
        for j in range(7):
            BDD[l+i,j]=BDD[l,j]
    
    
    xpath_fer="//div[contains(@class,'participants-details')]"
    fer=driver.find_elements_by_xpath(xpath_fer)
    n=len(fer)
    for i in range(n):
        BDD[l+i,8]=fer[i].text
    
    
    xpath_arrivee="//div[contains(@class,'participants-nav-region')]//li[contains(@class,'arrivee')]"
    element=driver.find_element_by_xpath(xpath_arrivee)
    element.click()
    
    xpath_option="//select[@id='participantsSelect']//option[text()='Numéro']"
    driver.find_element_by_xpath(xpath_option).click()
    
    xpath_tbody="//tr[contains(@class,'participants-tbody-tr')]"
    tbody_arrivee=driver.find_elements_by_xpath(xpath_tbody)
    n=len(tbody_arrivee)
    for i in range(n):
        BDD[l+i,9]=tbody_arrivee[i].text


    driver.execute_script("window.scrollTo(0,0)") 
    return(l+n)




def retrieve_place_information(j,l):
    try:
        xpath_place="//div[@class='bandeau-course-region']"
        elements=driver.find_element_by_xpath(xpath_place)
        number_of_races=len(elements.text.split('C'))-1
        l=retrieve_race_information(l)
        #print("number_of_races",number_of_races)
        for i in range(1,number_of_races):
            xpath_race="//li[contains(@class,'ARRIVEE')][@data-numordre='"+str(i+1)+"']"
            #print(xpath_race)
            driver.find_element_by_xpath(xpath_race).click()
            time.sleep(2)
            l=retrieve_race_information(l)
        xpath="//div[@class='bandeau-nav-content-scroll-item-numero']//span[contains(text(),'R"+str(j+1)+"')]"
        #print(xpath)
        driver.find_element_by_xpath(xpath).click()
        return(True,l)

    except NoSuchElementException:
        return(False,l)

    
def retrieve_day_information(l):
    place_exists=True    
    j=1

    while(place_exists):
        place_exists,l=retrieve_place_information(j,l)
        j+=1
        time.sleep(2)
    return(l)    

def retrieve_year_information(year):
    l=0
    for month in range(1,13):
        for day in range(1,29):
            if(month<10):
                str_month='0'+str(month)
            else:
                str_month=str(month)
            if(day<10):
                str_day='0'+str(day)
            else:
                str_day=str(day)
            driver.get('https://www.pmu.fr/turf/'+str_day+str_month+str(year)+'/R1/C1')
            time.sleep(2)
            l=retrieve_day_information(l)
   
   
##retrieve information from pmu website and store it into a numpy array

BDD_aux = np.zeros((100,10))
BDD = np.array(BDD_aux,dtype=object)
driver = webdriver.Chrome("C:/Users/Clément/Desktop/chromedriver.exe")            
retrieve_year_information(year)
driver.quit()

## Save the BDD to csv format
 
import pandas as pd 
df=pd.DataFrame(BDD,columns=["piste","hour","day","infos-course","infos-conditions","infos_meteo","meteo_icon","infos_partants","fer","infos_arrivee"])

df.to_csv('BDD_pmu_trot_'+str(year)+'.csv',columns=["piste","hour","day","infos-course","infos-conditions","infos_meteo","meteo_icon","infos_partants","fer","infos_arrivee"])
print(df.columns)

