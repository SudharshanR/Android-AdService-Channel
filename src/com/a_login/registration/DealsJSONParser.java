package com.a_login.registration;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/** A class to parse json data */
public class DealsJSONParser {
	
	// Receives a JSONObject and returns a list
	public List<HashMap<String,Object>> parse(JSONObject jObject){		
		
		JSONArray jCountries = null;
		try {		
			// Retrieves all the elements in the 'countries' array 
			jCountries = jObject.getJSONArray("products");
		} catch (JSONException e) {
			e.printStackTrace();
		}
		
		 // Invoking getCountries with the array of json object
		 // where each json object represent a country
		return getCountries(jCountries);
	}
	
	
	private List<HashMap<String, Object>> getCountries(JSONArray jCountries){
		int countryCount = jCountries.length();
		List<HashMap<String, Object>> countryList = new ArrayList<HashMap<String,Object>>();
		HashMap<String, Object> country = null;	

		// Taking each country, parses and adds to list object 
		for(int i=0; i<countryCount;i++){
			try {
				// Call getCountry with country JSON object to parse the country 
				country = getCountry((JSONObject)jCountries.get(i));
				countryList.add(country);

			} catch (JSONException e) {
				e.printStackTrace();
			}
		}
		
		return countryList;
	}
	
	// Parsing the Country JSON object 
	private HashMap<String, Object> getCountry(JSONObject jCountry){

		HashMap<String, Object> country = new HashMap<String, Object>();
		String countryName = "";
		String flag="";
		String language = "";
		String capital = "";
		String currencyCode = "";
		String currencyName = "";		
		
		try {
		/*	countryName = jCountry.getString("DealName");
			flag = jCountry.getString("ImageURL");
			language = jCountry.getString("Description")+" \n Price =$ "+jCountry.getString("Price");
		*/
			countryName = jCountry.getString("dealTitle");
			flag = jCountry.getString("showImage");
			//language = jCountry.getString("longDescription")+" \n Manufacturer : "+jCountry.getString("manufacturer");
			//language = "Description";
			language = " DealSource "+jCountry.getString("dealSource");
			country.put("country", countryName);
			country.put("flag", R.drawable.ic_launcher);
			country.put("flag_path", flag);
			country.put("language", language);
		} catch (JSONException e) {			
			e.printStackTrace();
		}		
		return country;
	}
}