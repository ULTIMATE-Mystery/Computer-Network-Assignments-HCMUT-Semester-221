package Main;

import GUI.LoginGUI;
import Handler.Server;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        LoginGUI r = new LoginGUI();
        Server.init();
    }
}
