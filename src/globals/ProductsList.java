package globals;

import java.util.ArrayList;

import bean.Product;
import android.graphics.Bitmap;

public class ProductsList{
	
	private static ProductsList instance;
	private ArrayList<Product> products;
	private ArrayList<Product> cart = new ArrayList<Product>();

	// Restrict the constructor from being instantiated
	private ProductsList(){}


	public static synchronized ProductsList getInstance(){
		if(instance==null){
			instance=new ProductsList();
		}
		return instance;
	}
	

	public Product getProductAt(int index) {
		return products.get(index);
	}

	public void setProducts(ArrayList<Product> products) {
		this.products = products;
	}
	
	public void addToCart(Product product){
		cart.add(product);
	}
	
	public ArrayList<Product> getCart(){
		return cart;
	}
}