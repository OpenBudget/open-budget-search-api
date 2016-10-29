open-budget-search-api
======================

Install:

	Elasticsearch part

		On windows:

		1. Download elasticsearch 1.7.0 from:
		https://www.elastic.co/downloads/past-releases/elasticsearch-1-7-0
		2. Go to the bin direcotry and execture:
		plugin --install analysis-hebrew --url https://bintray.com/artifact/download/synhershko/elasticsearch-analysis-hebrew/elasticsearch-analysis-hebrew-1.7.zip
		3. download all the hebrew data files from:
		https://github.com/synhershko/HebMorph/tree/master/hspell-data-files

		into plugins/analysis-hebrew/hspell-data-files

		4. Go to config\elasticsearch.yml and add at the buttom the following line:
		hebrew.dict.path: FULL/PATH/TO/HSPELL-DATA-FILES
		for example:
		hebrew.dict.path: C:\dev\elasticsearch-1.7.0\hspell-data-files\

		5. Now start elasticsearch bin\elasticsearch.bat, and via your browser test the plugin by going to :
		http://localhost:9200/_hebrew/check-word/בדיקה

		If it loads, it means everything is set up and you are good to go.

		6. If something in one of the steps is not working you may find help over elasticsearch website and 
		the hebrew plugin github repository.


		On Linux:

		1. Download latest elasticsearch version
		2. Go to the bin direcotry and execute:
		plugin install https://bintray.com/synhershko/elasticsearch-analysis-hebrew/download_file?file_path=elasticsearch-analysis-hebrew-2.3.4.zip
		3. download all the hebrew data files from:
		https://github.com/synhershko/HebMorph/tree/master/hspell-data-files

		into plugins/analysis-hebrew/hspell-data-files

		4. Go to config\elasticsearch.yml and add at the buttom the following line:
		hebrew.dict.path: FULL/PATH/TO/HSPELL-DATA-FILES
		for example:
		hebrew.dict.path: C:\dev\elasticsearch-1.7.0\hspell-data-files\

		5. Now start elasticsearch bin\elasticsearch.bat, and via your browser test the plugin by going to :
		http://localhost:9200/_hebrew/check-word/בדיקה

		If it loads, it means everything is set up and you are good to go.

		6. If something in one of the steps is not working you may find help over elasticsearch website and 
		the hebrew plugin github repository.
	

	run:

	open-budget-search-api part:
		
		1. Run init_db.py - This will load all of the tables that are under data/ directory
		The following tables are to be expected to be there:
			exemption, budget, supports, changes, type_name (change_history can also be put there). There rest
			of the tables will be ignored
		2. Run main.py -  This module start listening to requests of the following structure:
		http://localhost:8888/search/comma_seperated_table_names/search_term/from_data/to_date/maxinum_size_of_result/offset
		for example
		http://localhost:8888/search/exemption/test/2000-01-01/2019-01-01/4/0
		3. There is a log for exceptions called obudget.log which is written right next to the main.py and/or init_db
		
		
		
	
	
	
	
