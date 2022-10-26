
package functions;

import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;
import java.io.BufferedWriter;
import java.io.IOException;

public class Java implements HttpFunction {
  // Simple function to return "Hello from Archy in Java!"
  @Override
  public void service(HttpRequest request, HttpResponse response)
      throws IOException {
    BufferedWriter writer = response.getWriter();
    writer.write("Hello from Archy in Java!");
  }
}
