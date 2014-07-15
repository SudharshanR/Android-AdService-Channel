package globals;

import android.graphics.Bitmap;
import android.os.Parcel;
import android.os.Parcelable;

public class ImgDetails implements Parcelable {

	private String title;
	private String description;
	private Bitmap image;
	
	public ImgDetails(String title, String description, Bitmap image){
		this.title = title;
		this.description = description;
		this.image = image;
	}
	
	public String getTitle(){
		return title;
	}
	
	public String getDescription(){
		return description;
	}
	
	public Bitmap getImage(){
		return image;
	}

	@Override
	public int describeContents() {
		return 0;
	}

	@Override
	public void writeToParcel(Parcel dest, int flags) {
		dest.writeString(title);
		dest.writeString(description);
		image.writeToParcel(dest, 0);
		dest.setDataPosition(0);
		
	} 
	
	public static final Parcelable.Creator<ImgDetails> CREATOR = new Parcelable.Creator<ImgDetails>() {
		
        public ImgDetails createFromParcel(Parcel in) {
            return new ImgDetails(in);
        }

        public ImgDetails[] newArray(int size) {
            return new ImgDetails[size];
        }
    };

    // example constructor that takes a Parcel and gives you an object populated with it's values
    private ImgDetails(Parcel in) {
        title = in.readString();
        description = in.readString();
        image = Bitmap.CREATOR.createFromParcel(in);
    }
}
