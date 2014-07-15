package com.a_login.registration;

import java.util.HashMap;

import android.util.Log;

public class PassItem {
	 public String newText;
	 HashMap<String, Object> s;
	  public PassItem(String newText) {
	      this.newText = newText;
	  	Log.d("Sagar", "inside constructor");

	  }
	public PassItem(HashMap<String, Object> s) {
		// TODO Auto-generated constructor stub
		this.s=s;
	}
}
