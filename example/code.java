    public void sendGuess(String guess) {
      if( isConnected() ) {
        gui.statusBarInfo("Querying...", false);
        try {
          os.write( (guess + "\\r\\n").getBytes() );
          os.flush();
        } catch (IOException e) {
    gui.statusBarInfo(
        "Failed to send guess.IOException",true
        );
    System.err.println(
        "IOException during send guess to server"
        );
        }
      }
    }
