package xprolog;

//////////////////////////////////////////////////////
//
//  PostOffice.java:  Dispatcher for messages between Prolog Agents.
//  ================
//  Author: J. Vaucher (vaucher@iro.umontreal.ca)
//  Date: 2002/5/10
//  URL:  www.iro.umontreal.ca/~vaucher/~XProlog
//

import java.util.ArrayList;
import java.util.List;

public class PostOffice {

    static ArrayList agents = new ArrayList();

    public static int register(List l) {
        agents.add(l);
        return agents.size() - 1;
    }

    public static void send(int src, int dest, Term msg) {
        if (dest >= agents.size())
            return;
        Message m = new Message(src, msg);
        List l = (List) agents.get(dest);
        l.add(m);
    }

    public static void broadcast(int src, Term msg) {
        Message m = new Message(src, msg);

        for (int i = 0; i < agents.size(); i++) {
            List l = (List) agents.get(i);
            l.add(new Message(src, msg));
        }
    }

}

class Message {
    int source;

    Term content;

    public Message(int s, Term m) {
        source = s;
        content = m;
    }

    public String toString() {
        return source + ":" + content;
    }
}
