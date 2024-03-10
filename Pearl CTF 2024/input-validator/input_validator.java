import java.util.Scanner;

public class input_validator {
   private static final int FLAG_LEN = 34;

   private static boolean validate(String var0, String var1) {
      int[] var2 = new int[34];
      int[] var3 = new int[]{1102, 1067, 1032, 1562, 1612, 1257, 1562, 1067, 1012, 902, 882, 1397, 1472, 1312, 1442, 1582, 1067, 1263, 1363, 1413, 1379, 1311, 1187, 1285, 1217, 1313, 1297, 1431, 1137, 1273, 1161, 1339, 1267, 1427};

      int var4;
      for(var4 = 0; var4 < 34; ++var4) {
         var2[var4] = var0.charAt(var4) ^ var1.charAt(var4);
      }

      for(var4 = 0; var4 < 34; ++var4) {
         var2[var4] -= var1.charAt(33 - var4);
      }

      int[] var6 = new int[34];

      int var5;
      for(var5 = 0; var5 < 17; ++var5) {
         var6[var5] = var2[1 + var5 * 2] * 5;
         var6[var5 + 17] = var2[var5 * 2] * 2;
      }

      for(var5 = 0; var5 < 34; ++var5) {
         var6[var5] += 1337;
      }

      for(var5 = 0; var5 < 34; ++var5) {
         if (var6[var5] != var3[var5]) {
            return false;
         }
      }

      return true;
   }

   public static void main(String[] var0) {
      Scanner var1 = new Scanner(System.in);
      String var2 = "oF/M5BK_U<rqxCf8zWCPC(RK,/B'v3uARD";
      System.out.print("Enter input: ");
      String var3 = var1.nextLine();
      if (var3.length() != 34) {
         System.out.println("Input length does not match!");
      } else {
         if (validate(new String(var3), var2)) {
            System.out.println("Correct");
         } else {
            System.out.println("Wrong");
         }

      }
   }
}
