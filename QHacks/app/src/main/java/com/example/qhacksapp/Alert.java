package com.example.qhacksapp;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class Alert extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_alert);
        Intent intent = getIntent();
        String message = intent.getStringExtra(MainActivity.EXTRA_MESSAGE);
//        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(this);
//        System.out.println("ALERT ");
////                Thread.currentThread().suspend();
//        alertDialogBuilder.setMessage(message)
//                .setTitle("Incoming Vehicle!");
//        AlertDialog dialog = alertDialogBuilder.create();
        TextView textView = (TextView) findViewById(R.id.alert);
        textView.setText("WARNING: Car approaching from " + message);

        Button button= (Button) findViewById(R.id.ret);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                startActivity(new Intent(Alert.this, MainActivity.class));
            }
        });

//                Thread.currentThread().resume();
    }
}