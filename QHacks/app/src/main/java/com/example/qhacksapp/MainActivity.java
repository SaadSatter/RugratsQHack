package com.example.qhacksapp;

import static android.hardware.SensorManager.AXIS_Z;
import static android.provider.AlarmClock.EXTRA_MESSAGE;
import static android.view.MotionEvent.AXIS_X;
import static java.lang.System.exit;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity implements SensorEventListener {
    private SensorManager sensorManager;
    private Sensor mRotationV, mAccelerometer, mMagnetometer;
    private float mAzimuth;
    private float[] accelerometerReading = new float[3];
    private float[] magnetometerReading = new float[3];

    private float[] rotationMatrix = new float[9];
    private Double prev_lat, prev_lon;
    private float[] orientationAngles = new float[9];
    private boolean haveSensor, haveSensor2, isAccelerometer, isMagnemeterSet;
    private boolean azimuthChanged;
    public static final String EXTRA_MESSAGE = "com.example.qhacksapp.MESSAGE";
    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ActivityResultLauncher<String[]> locationPermissionRequest =
                registerForActivityResult(new ActivityResultContracts
                                .RequestMultiplePermissions(), result -> {
                            Boolean fineLocationGranted = result.getOrDefault(
                                    Manifest.permission.ACCESS_FINE_LOCATION, false);
                            Boolean coarseLocationGranted = result.getOrDefault(
                                    Manifest.permission.ACCESS_COARSE_LOCATION,false);
                            if (fineLocationGranted != null && fineLocationGranted) {
                                // Precise location access granted.
                            } else if (coarseLocationGranted != null && coarseLocationGranted) {
                                // Only approximate location access granted.
                            } else {
                                // No location access granted.
                            }
                        }
                );

        // ...
//        Intent intent = new Intent(this, Alert.class);
//        intent.putExtra(EXTRA_MESSAGE,"FRONT!");
//        stop();
//        startActivity(intent);

        // Before you perform the actual permission request, check whether your app
        // already has the permissions, and whether your app needs to show a permission
        // rationale dialog. For more details, see Request permissions.
        locationPermissionRequest.launch(new String[] {
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_COARSE_LOCATION
        });
//        TextView editText = (TextView) findViewById(R.id.hello);
//        editText.setText("Waiting For Signal");

    }


    @Override
    public void onResume(){
        super.onResume();
        PyObject output = null;
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        start();
        Double angle = -1.0;
        prev_lat = 0.0;
        prev_lon = 0.0;


    }

    // Get readings from accelerometer and magnetometer. To simplify calculations,
    // consider storing these readings as unit vectors.
    @Override
    public void onSensorChanged(SensorEvent event) {

        if(event.sensor.getType() == Sensor.TYPE_ROTATION_VECTOR){
            SensorManager.getRotationMatrixFromVector(rotationMatrix,event.values);
            mAzimuth = (float) ((Math.toDegrees(SensorManager.getOrientation(rotationMatrix,orientationAngles)[0])*360)%360);
//            System.out.println("Sensor Changed " + mAzimuth);
            azimuthChanged = true;
            Log.i("ssatter", "Changed: " + mAzimuth);
        }
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            System.arraycopy(event.values, 0, accelerometerReading,
                    0, event.values.length);
            isAccelerometer = true;
        } else if (event.sensor.getType() == Sensor.TYPE_MAGNETIC_FIELD) {
            System.arraycopy(event.values, 0, magnetometerReading,
                    0, event.values.length);
            isMagnemeterSet = true;
        }
        if(isAccelerometer && isMagnemeterSet){
            SensorManager.getRotationMatrix(rotationMatrix, null, accelerometerReading, magnetometerReading);
            SensorManager.getOrientation(rotationMatrix, orientationAngles);
            mAzimuth = (float) ((Math.toDegrees(SensorManager.getOrientation(rotationMatrix,orientationAngles)[0])*360)%360);
            azimuthChanged = true;
            Log.i("ssatter", "Changed: " + mAzimuth);


        }

        mAzimuth= Math.round(mAzimuth) *-1;
        System.out.println("Sensor Changed " + mAzimuth);
        Log.i("ssatter", "Changed: " + mAzimuth);
        if(azimuthChanged){
            runStuff(azimuthChanged);

        }


    }
    public void runStuff(Boolean azimuthChanged){
        PyObject output = null;
        Double angle = -1.0;
        GPSTracker gpsTracker = new GPSTracker(getApplicationContext());
//            Log.i("ssatter", "PROBLEM");


//            Sensor accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
//
//            if (accelerometer != null) {
//                sensorManager.registerListener(this, accelerometer,
//                        SensorManager.SENSOR_DELAY_NORMAL, SensorManager.SENSOR_DELAY_UI);
//            }
//            Sensor magneticField = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
//            if (magneticField != null) {
//                sensorManager.registerListener(this, magneticField,
//                        SensorManager.SENSOR_DELAY_NORMAL, SensorManager.SENSOR_DELAY_UI);
//            }

// Express the updated rotation matrix as three orientation angles.
        float[] orientationAngle = new float[3];
//            updateOrientationAngles();
//            orientationAngle = SensorManager.getOrientation(rotationMatrix, orientationAngles);
        Location location = gpsTracker.getLocation();
        String temp = gpsTracker.getLatitude() + ", " + gpsTracker.getLongitude();
        System.out.println(temp);
        Boolean x = azimuthChanged;
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        Python py = Python.getInstance();
        PyObject pyobj = py.getModule("main");
        angle =  (double) mAzimuth;
        output = pyobj.callAttr("main", prev_lat, prev_lon, gpsTracker.getLatitude(), gpsTracker.getLongitude(), angle);


//            final float[] orientation = orientationAngles;



//            editText.setText(output.toString() + "\n" + orientationAngles[0]);
        try {
            TimeUnit.SECONDS.sleep(10);
        } catch (InterruptedException e) {
            e.printStackTrace();
            Log.e("BAD: ", "EEEERRRRORR");
        }
        if(!azimuthChanged){
            System.out.println("azimuth not changed");
            Log.i("BAD: ", angle.toString());
        }
        else {
            Log.i("AZIMUTH: ", angle.toString());
        }
//            if((output.toString().contains("Intersect"))){
//                break;
//            }
        Log.d("WHILE: ", x.toString());

        Log.d("WHILE: ", x.toString());
        Log.d("ANGLE: ", angle.toString());
        System.out.println("Start New Activity");
        if(output.toString().contains(",")){
            String[] convertedRankArray = output.toString().split(",");
            List<Double> convertedRankList = new ArrayList<Double>();
            for (String number : convertedRankArray) {
                convertedRankList.add(Double.parseDouble(number.trim()));
            }
            prev_lat = convertedRankList.get(0);
            prev_lon = convertedRankList.get(1);
        }
        if(output.toString().contains("Intersect")) {
            Intent intent = new Intent(this, Alert.class);
            intent.putExtra(EXTRA_MESSAGE, output.toString().substring(output.toString().indexOf('\n')));
            stop();
            startActivity(intent);
        }

    }
    @Override
    public void onPause(){
        super.onPause();
        Log.d("HI: ", "PAUSING");
        stop();
    }

    public void start(){
        if(sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR) == null){

            if(sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) == null){
                System.out.println("NO SENSOR");
            }
        }
        else if(sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null) {
            mAccelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            mMagnetometer = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
            haveSensor = sensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_UI);
            haveSensor2 = sensorManager.registerListener(this, mMagnetometer, SensorManager.SENSOR_DELAY_UI);
        }
        else {
            mRotationV = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);
            haveSensor = sensorManager.registerListener(this, mRotationV, SensorManager.SENSOR_DELAY_UI);
        }

    }

    public void stop(){
        if(haveSensor2) {
            Log.d("HI: ", "PAUSING SENSORS");
            sensorManager.unregisterListener(this, mAccelerometer);
            sensorManager.unregisterListener(this, mMagnetometer);
        }
        else{
            sensorManager.unregisterListener(this,mRotationV);
        }

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
    // Compute the three orientation angles based on the most recent readings from
    // the device's accelerometer and magnetometer.
    public void updateOrientationAngles() {
        // Update rotation matrix, which is needed to update orientation angles.
        SensorManager.getRotationMatrix(rotationMatrix, null,
                accelerometerReading, magnetometerReading);

        // "rotationMatrix" now has up-to-date information.
//        SensorManager.remapCoordinateSystem(inR, AXIS_X, AXIS_Z, outR);
        SensorManager.getOrientation(rotationMatrix, orientationAngles);

        // "orientationAngles" now has up-to-date information.
    }

}