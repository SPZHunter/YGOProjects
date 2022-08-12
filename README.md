# YGOProjects
Repository for Yu-Gi-Oh Projects

#### **Project Scope/Requirements**
 - The idea is that multiple projects can benefit from tools in this repo.
 - MiniDeckList is the first, and obviously needs certain information
     - Namely card type and an image
     - This data needs to be obtained with a web scraper and stored in an
       object
 - The aim is to build tools (such as the scraper) and objects (such as the
   deck list) which can be useful for other potential projects, so try and
   write code with that in mind.
 - As an example, the mini deck list does not need a level for a monster, but
   it would be useful to have that data avaliable in future.

#### **Project Environment**
 - YGOProjects.yml should be used for virtual environment creation. 
 - If adding to/changing the environment please remember to update the .yml. 
   ```
   conda env export --no-builds | findstr -v "^prefix" > environemnt.yml
   ```
   or
   ```
   conda env export --no-builds | grep -v "^prefix" > environemnt.yml
   ```
 - You can update your environment and remove unused dependencies with:
    ```
    conda activate myenv
    conda env update --file local.yml --prune
    ```

#### **Project List**Environment
 - MiniDeckList

