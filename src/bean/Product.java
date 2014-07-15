package bean;

import android.graphics.Bitmap;

public class Product{

	private String title;
	private String description;
	private Bitmap image;
	private double price;
	private boolean selected;

	// Restrict the constructor from being instantiated
	public Product(String title, String description, double price, Bitmap image){
		this.title = title;
		this.description = description;
		this.image = image;
		this.price = price;
	}


	public String getTitle() {
		return title;
	}

	public String getDescription() {
		return description;
	}

	public double getPrice() {
		return price;
	}

	public double getEstimatedTaxMicros() {
		return (int) (price * 0.10);
	}

	public double getEstimatedShippingPriceMicros() {
		return 10000000L;
	}

	public double getTaxMicros() {
		return (int) (price * 0.10);
	}

	public double getShippingPriceMicros() {
		return price;
	}

	 public double getTotalPrice() {
	     return price + getTaxMicros() + getShippingPriceMicros();
	 }

	public Bitmap getImage() {
		return image;
	}
	
	public boolean isSelected(){
		return selected;
	}
	
	public void setSelected(boolean select){
		this.selected = select;
	}
}