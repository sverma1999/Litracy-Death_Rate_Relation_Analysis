#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np    
import matplotlib.pyplot as plt, mpld3
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from tornado.web import RequestHandler, Application

import bs4



class Ldt_Dyn_Relation:
    
    def __init__(self):
        self.dRate = pd.DataFrame()
        self.lRate = pd.DataFrame()
        self.pearson_coefficient = 0
        self.p_valueOfPearson = 0
        self.spearman_coefficient = 0
        self.p_valueOfSpearman = 0
        self.fig = ''
        self.temp = []
        self.temp2 = []
    def deathRate(self):
        data = pd.read_excel("Death_Rate.xlsx", sheet_name=0)
        south_asia = data.query('Country_Name == "South Asia"')
        self.temp = south_asia
        self.dRate = self.dataFrameToArray(south_asia)
        self.dRate
        
    def litracyRate(self):
        data = pd.read_excel("Litracy_Rate.xlsx", sheet_name=0)
        south_asia = data.query('Country_Name == "South Asia"')
        self.temp2 = south_asia
        self.lRate = self.dataFrameToArray(south_asia)
        self.lRate

    def dataFrameToArray(self, df):
        dfToArr = df.iloc[:, 4:]
        dfToArr.fillna(0, inplace = True)
        return dfToArr.to_numpy()
    
    def runProgram(self):
        self.deathRate()
        self.litracyRate()
        self.findCorrelations()
    
    def graphFigure(self):
       
        self.fig = plt.figure(figsize=(15, 10))
        plt.ylim(5,16)
        plt.xlim(35,74)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.xlabel("Litracy Rate of people above ages 15", fontsize=20)
        plt.ylabel("Death Rate (per 1000 people)", fontsize=20)
        l = self.getInnerArray(self.lRate)
        d = self.getInnerArray(self.dRate)
        plt.scatter(l, d, s=100)
        #self.figOnWeb(fig)
        #webFigure = mpld3.fig_to_html(fig)
        print(type(self.fig))
        plt.show()
            

    def findCorrelations(self):
        self.pearsonCorrelation(self.lRate, self.dRate)
        self.spearmanCorrelation(self.lRate, self.dRate)
    
    def pearsonCorrelation(self, variableOne, variableTwo):
        vOne = self.getInnerArray(variableOne)
        vTwo = self.getInnerArray(variableTwo)
        self.pearson_coefficient, self.p_valueOfPearson = pearsonr(vOne,vTwo)
        
    
    def spearmanCorrelation(self, variableOne, variableTwo):
        vOne = self.getInnerArray(variableOne)
        vTwo = self.getInnerArray(variableTwo)
        self.spearman_coefficient, self.p_valueOfSpearman = spearmanr(vOne,vTwo)
        
    def getInnerArray(self, var):
        arr = []
        for i in var:
            for a in i:
                arr.append(a)
        return arr
    
    def getYears(self, d):
        f = []
        for i in d:
            f.append(int(i))
        return f   
    
    
    def getSeparateGraphs(self):
        #firstgraph
        lit = self.temp2.iloc[:, 4:]
        lit.fillna(0, inplace = True)
        years = self.getYears(lit)
        lr = self.getInnerArray(self.lRate)
            
        fig1 = plt.figure(figsize=(10, 7))
        plt.xlabel("Years", fontsize=18)
        plt.ylabel("Litracy Rate (from total yearly population)", fontsize=18)
        plt.title("Change in litracy rate over the years", fontsize=20)
        plt.bar(years,lr, color = 'c')

        #secondgraph 
        lit = self.temp.iloc[:, 4:]
        lit.fillna(0, inplace = True)
        years = self.getYears(lit)
        dr = self.getInnerArray(self.dRate)

        fig2 =plt.figure(figsize=(10, 7))
        plt.xlabel("Years", fontsize=18)
        plt.ylabel("Death Rate (per 1000 people)", fontsize=18)
        plt.title("Change in death rate over the years", fontsize=20)
        plt.bar(years,dr, color = 'c')
        
        #save these figures in html page
        self.HomePage(fig1, fig2)
    
    def HomePage(self, fig1, fig2):
        # create html for both graphs 
        html1 = mpld3.fig_to_html(fig1)
        html2 = mpld3.fig_to_html(fig2)
        # save joined html to html file
        h1_tag = '<h1 style="text-align:center; color: chocolate"> Literacy Rate vs Death Rate</h1>'
        link_tag = '<a href="correlation/" style="position:absolute; top:550px; left:800px;font-size:40px;">Click here to check the relation betweem them!</a>'
        html_str = h1_tag + html1 + html2 + link_tag
        fileName = 'index.html' 
        Html_file= open(fileName,"w")
        Html_file.write(html_str)
        Html_file.close() 

    
    
    

relation = Ldt_Dyn_Relation()
relation.runProgram()
relation.getSeparateGraphs()
relation.graphFigure()
f = relation.fig



class FirstPage(RequestHandler):
    def get(self):
        fileName = 'index.html' 
        self.render(fileName)

class SecondPage(RequestHandler):
  
    def get(self):       
        fileName = 'correlation.html'
        mpld3.save_html(f, fileName)
        self.edit(fileName)
        self.render(fileName)
 
    def edit(self, fileName):
        # load the file
        with open(fileName) as inf:
            txt = inf.read()
            soup = bs4.BeautifulSoup(txt)
         
        soup = self.insert_in_head(soup)
        self.insert_in_body(soup)
        
        # save the file again
        with open(fileName, "w") as outf:
            outf.write(str(soup))            
            
    def insert_in_head(self, soup):
        # insert tags into the head
        h1_tag = soup.new_tag("h1", style="text-align:center; color: chocolate")
        # insert heading into the h1_tag
        h1_heading = 'Relation Between Death Rate and Literacy  Rate from 1960 to 2018'
        h1_tag.append(h1_heading)        
        # insert it into the head
        soup.head.append(h1_tag)
        return soup
        
    def insert_in_body(self, soup):
        # insert tags into the body
        self.pearson_corr(soup)
                
        # insert tags into the body
        self.spearman_corr(soup)
        
        
    def pearson_corr(self, soup):
        #Pearson Correlations 
        h2_tag = soup.new_tag("h2", style="text-align:center; color: chocolate;")
        # insert heading into the h2_tag
        h2_heading = 'Pearson Correlation'
        h2_tag.append(h2_heading)
        # create paragraph into the body_tags 
        pearson_para = soup.new_tag("p", style="text-align:center")
        para1 = 'Correlation Value: {:7.4}'.format(relation.pearson_coefficient)
        pearson_para.append(para1)
        pearson_para_br = soup.new_tag("br")
        pearson_para.append(pearson_para_br)
        after_br = 'p-Value: {:7.5}'.format(relation.p_valueOfPearson)
        pearson_para.append(after_br)
        
        #insert correletions and p-values into the  body
        soup.body.append(h2_tag)
        soup.body.append(pearson_para)
        
    
    def spearman_corr(self, soup):
        #Spearman Correlations 
        h2_tag2 = soup.new_tag("h2", style="text-align:center; color: chocolate;")
        # insert heading into the h2_tag
        h2_heading2 = 'Spearman Correlation'
        h2_tag2.append(h2_heading2)
        # create paragraph into the body_tags 
        spearman_para = soup.new_tag("p", style="text-align:center")
        para2 = 'Correlation Value: {:7.4}'.format(relation.spearman_coefficient)
        spearman_para.append(para2)
        spearman_para_br = soup.new_tag("br")
        spearman_para.append(spearman_para_br)
        after_br2 = 'p-Value: {:7.5}'.format(relation.p_valueOfSpearman)
        spearman_para.append(after_br2)
        
        #insert correlations and p-values into the  body
        soup.body.append(h2_tag2)
        soup.body.append(spearman_para)
   
    
def make_app():
    first_page = ("/3543598/", FirstPage)
    second_page = ("/3543598/correlation/", SecondPage)
    all_paths = [first_page, second_page]
    return Application(all_paths)

if __name__ == "__main__":
    app = make_app()
    server = app.listen(5240)  

