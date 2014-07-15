package com.a_login.registration;


import com.a_login.registration.Iwantscreen3.OnListItemSelected;
import android.os.Bundle;
import android.annotation.SuppressLint;
import android.app.ActionBar;
import android.app.FragmentTransaction;
import android.app.ActionBar.Tab;
import android.app.ActionBar.TabListener;
import android.content.Intent;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;

@SuppressLint("NewApi")
public class IwantActivity extends ActionBarActivity implements TabListener,OnListItemSelected {
	ViewPager viewPager;
	ActionBar actionBar;
	SessionManager session;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_iwant);
		session = new SessionManager(getApplicationContext());
		actionBar = getActionBar();
		actionBar.setDisplayHomeAsUpEnabled(true);
		actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);
		viewPager = (ViewPager) findViewById(R.id.iwant_pager);
		viewPager.setAdapter(new MyAdapter(getSupportFragmentManager()));
		//for synchronising the tabs and the action bar.
		viewPager.setOnPageChangeListener(new ViewPager.OnPageChangeListener() {
			
			@Override
			public void onPageSelected(int arg0) {
				// TODO Auto-generated method stub
				//same tab as the page 
				actionBar.setSelectedNavigationItem(arg0);
			}
			
			@Override
			public void onPageScrolled(int arg0, float arg1, int arg2) {
				// TODO Auto-generated method stub
				
			}
			
			@Override
			public void onPageScrollStateChanged(int arg0) {
				// TODO Auto-generated method stub
				
			}
		});
		
		actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);
		ActionBar.Tab tab3 = actionBar.newTab();
		tab3.setText("I want Search");
		tab3.setTabListener(this);
		
		//ActionBar.Tab tab4 = actionBar.newTab();
		//tab4.setText("I want Results");
		/*//tab4.setTabListener(this);
		
		ActionBar.Tab tab5 = actionBar.newTab();
		tab5.setText("Detailed Description");
		tab5.setTabListener(this);*/
		
		ActionBar.Tab tab6 = actionBar.newTab();
		tab6.setText("Bidding");
		tab6.setTabListener(this);
		
	//	ActionBar.Tab tab6 = actionBar.newTab();
		//tab6.setText("Bidding");
		//tab6.setTabListener(this);
		
		
		actionBar.addTab(tab3);
		//actionBar.addTab(tab4);
		//actionBar.addTab(tab5);
		//actionBar.addTab(tab6);
		actionBar.addTab(tab6);


	}

	@Override
	public void onTabReselected(Tab arg0, FragmentTransaction arg1) {
		// TODO Auto-generated method stub
		
	}

	@SuppressLint("NewApi")
	@Override
	public void onTabSelected(Tab tab, FragmentTransaction arg1) {
		// TODO Auto-generated method stub
		//for tab selected; corresponding action bar is selected
		viewPager.setCurrentItem(tab.getPosition());
		
	}

	@Override
	public void onTabUnselected(Tab arg0, FragmentTransaction arg1) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		switch (id){
		case R.id.action_cart:
		    Intent viewShoppingCartIntent = new Intent(getBaseContext(), ShoppingCartActivity.class);
		    startActivity(viewShoppingCartIntent);		   
			return true;
		case R.id.action_logout:
			session.logoutUser();
		    Intent homePage = new Intent(getBaseContext(), MainActivity.class);
		    startActivity(homePage);
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}
	}

	@Override
	public void onProductSelected(int position) {
		/*Bundle bundle = new Bundle();
		bundle.putParcelable("img_details", imgDetails);*/
		
		Intent intent = new Intent(this, ProductDetailsActivity.class);
		intent.putExtra("com.a_login.registration.IwantActivity.position", position);
		startActivity(intent);		
	}

}

class MyAdapter extends FragmentPagerAdapter{

	public MyAdapter(FragmentManager fm) {
		super(fm);
		// TODO Auto-generated constructor stub
	}

	@Override
	public Fragment getItem(int i) {
		// TODO Auto-generated method stub
		Fragment f=null;
		
		if(i==0){
			return f= new Iwantscreen3();
		}
		if(i==1){
			return f= new Bidding();
		}
		
		return f;
	}

	@Override
	public int getCount() {
		// TODO Auto-generated method stub
		return 2;
	}
	
	
}
