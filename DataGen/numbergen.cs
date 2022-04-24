using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;

class Generate{
    //Variable Declaration
    static string outPath;
    static bool addErrors;
    const string randomNames = "./RandomData.txt";
    static int count;
    static Contact[] contacts;
    static Stopwatch stopwatch = new Stopwatch();
    static List<string> fName, lName, numCodes;
    static Random rnd = new Random();

    //Main method, executes in O(n)
    public static int Main(string[] args){
        //Initialize and start
        stopwatch = new Stopwatch();
        stopwatch.Start();

        //Checks if argument count is valid
        if(args.Length != 3 && args.Length != 2){
            PrintERR("Usage: ./PhoneNumberGen <count> <toPath> -[mode]\n");
            return -1;
        }

        //Checks if count is a valid number
        int.TryParse(args[0], out count);
        if(count <= 0){
            PrintERR("Count must be a positive integer.\n");
            Console.Write("Usage: ./PhoneNumberGen <count> <toPath> [-mode]\n");
            return -1;
        }

        //Checks if paths are valid, creates file at outPath
        outPath = args[1];
        if(!outPath.Contains(".csv")){
            PrintERR(String.Format("\"{0}\" must be a path to a csv file.", outPath));
            return -1;
        }

        //Checks if running mode is valid
        if(args.Length == 3){
            addErrors = args[2].ToLower() == "-e";
            if(!addErrors){
                PrintERR("Mode must be \'e\' if you wish to add errors in generated data.\n");
                Console.Write("Usage: ./PhoneNumberGen <count> <toPath> [-mode]\n");
                return 0;
            }
        }

        //Initialize Data Structures
        contacts = new Contact[count]; 
        fName = new List<string>();
        lName = new List<string>();
        numCodes = new List<string>{
            "+91",    //India
            "+1-268",  //Barbuda
            "+244",     //Angola
            "+685",     //Samoa
            "+61",      //Australia
            "+1-809",   //Dominican Republic
            "+1-829",   //Dominican Republic
            "+1-849",   //Dominican Republic
            "+44-1481", //Guernsey
            "+81",    //Japan
            "+1-242", //Bahamas
            "+1",     //United States
        };

        //Read from CSV file
        using(var sr = new StreamReader(randomNames)){
            while(!sr.EndOfStream){
                var line = sr.ReadLine();
                var values = line.Split(' ');

                fName.Add(values[0]);
                lName.Add(values[1]);
            }
        }

        //Write To Array of structs
        for(int i = 0; i < count; i++){
            string name, num;

            name = SelectRandom(fName) + " " + SelectRandom(lName);
            num = GenerateRandomNumber(addErrors);

            contacts[i].Name = name;
            contacts[i].Num = num;
        }

        //Write to CSV File
        using(var sw = new StreamWriter(outPath)){
            foreach(var contact in contacts){
                sw.WriteLine("{0},{1}", contact.Name, contact.Num);
            }
        }

        //Stop the stopwatch and print result
        stopwatch.Stop();
        PrintSUC(String.Format("Generated {0} conatcts in {1}ms at file \"{2}\".\n", count, stopwatch.ElapsedMilliseconds, outPath));
        if(addErrors){
            Console.WriteLine("Data will have random errors.");
        }

        //End of program
        return 0;
    }

    //Generates a random number and returns it as a string
    public static string GenerateRandomNumber(bool err){
        //Variable Declaration
        string[] segments;
        string numCode;
        int error;
        segments = new string[3];

        numCode = SelectRandom(numCodes);
        segments[0] = rnd.Next(100, 999).ToString();
        segments[1] = rnd.Next(1000, 9999).ToString();
        segments[2] = rnd.Next(100, 999).ToString();

        //Return a number without any errors
        if(!err){
            return numCode + " " + segments[0] + segments[1] + segments[2]; //Return a normally formatted number
        }

        //Create Number with an error
        error = rnd.Next(8);
        switch (error){
            case 0:
                return numCode + "-" + segments[0] + "-" + segments[1] + "-" + segments[2]; //Number will have -'s in between each segment
            case 1:
                return numCode + " " + segments[0] + " " + segments[1] + " " + segments[2]; //Number will have spaces in between each segment
            case 2:
                return numCode + segments[0] + "-" + segments[1] + "-" + segments[2]; //Number's country code will not be formatted
            case 3:
                return numCode.Replace("+", "" ) + "-" + segments[0] + "-" + segments[1] + "-" + segments[2]; //Number's country code will not have +, dash formatting
            case 4:
                return numCode.Replace("+", "") + " " + segments[0] + " " + segments[1] + " " + segments[2]; //Number's country code will not have +, space formatting
            case 5:
                return numCode.Replace("+", "") + segments[0] + segments[1] + segments[2]; //Number's country code will not have + and number wont be formatted
            case 6:
                return segments[0] + "-" + segments[1] + "-" + segments[2]; //Number will have no country code and be formatted with dashes
            case 7:
                return segments[0] + " " + segments[1] + " " + segments[2]; //Number will have no country code and be formatted with spaces
            case 8:
                return segments[0] + segments[1] + segments[2]; //Number will have no country code or formatting
            default:
                return "";
        }
    }

    //Selects a random element from li and returns it
    public static string SelectRandom(List<string> li){
        string choice;
        choice = li[rnd.Next(li.Count - 1)];
        return choice;
    }

    //Print Colour: Print a message in colour
    static void PrintC(string output, ConsoleColor colour){
        Console.ForegroundColor = colour;
        Console.Write(output);
        Console.ForegroundColor = ConsoleColor.Gray;
    }

    //Print Error: Prints a formatted error message
    static void PrintERR(string message){
        Console.Write('[');
        PrintC("ERROR", ConsoleColor.Red);
        Console.Write("]: ");
        Console.Write(message);
    }

    //Print Success: Prints a formatted success message
    public static void PrintSUC(string message){
        Console.Write('[');
        PrintC("SUCCESS", ConsoleColor.Green);
        Console.Write("]: ");
        Console.Write(message);
    }
}


public struct Contact{
    public string Name, Num;
}
