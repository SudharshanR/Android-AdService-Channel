package com.a_login.registration;

import globals.ProductsList;

import java.util.List;

import bean.Product;
import adapter.ProductAdapter;
import android.support.v7.app.ActionBarActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.TextView;

public class ShoppingCartActivity extends ActionBarActivity {

	private List<Product> mCartList;
	private ProductAdapter mProductAdapter;
	private ProductsList productsList;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_shopping_cart);

		productsList = ProductsList.getInstance();

		mCartList = productsList.getCart();

		// Make sure to clear the selections
		for(int i=0; i<mCartList.size(); i++) {
			mCartList.get(i).setSelected(false);
		}

		// Create the list
		final ListView listViewCatalog = (ListView) findViewById(R.id.ListViewCatalog);
		
		TextView emptyCart = (TextView) findViewById(R.id.emptyCart);
		
		if(mCartList.size() == 0){
			emptyCart.setVisibility(View.VISIBLE);
		}
		else{
			listViewCatalog.setVisibility(View.VISIBLE);
			mProductAdapter = new ProductAdapter(mCartList, getLayoutInflater(), true);
			listViewCatalog.setAdapter(mProductAdapter);
			listViewCatalog.setOnItemClickListener(new OnItemClickListener() {

				@Override
				public void onItemClick(AdapterView<?> parent, View view, int position,
						long id) {

					Product selectedProduct = mCartList.get(position);
					if(selectedProduct.isSelected() == true)
						selectedProduct.setSelected(false);
					else
						selectedProduct.setSelected(true);

					mProductAdapter.notifyDataSetInvalidated();

				}
			});			
		}

		Button removeButton = (Button) findViewById(R.id.ButtonRemoveFromCart);
		removeButton.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				// Loop through and remove all the products that are selected
				// Loop backwards so that the remove works correctly
				for(int i=mCartList.size()-1; i>=0; i--) {

					if(mCartList.get(i).isSelected()) {
						mCartList.remove(i);
					}
				}
				mProductAdapter.notifyDataSetChanged();
			}
		});

		Button checkout = (Button) findViewById(R.id.checkoutButton);
		checkout.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				Intent intent = new Intent(ShoppingCartActivity.this, SetCheckoutActivity.class);
				startActivity(intent);
			}
		});

	}

}
