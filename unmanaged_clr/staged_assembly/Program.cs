using System;
using System.Windows.Forms;

namespace staged_assembly
{
    public class Program
    {
        static int EntryPoint(String pwzArgument)
        {
            System.Media.SystemSounds.Beep.Play();

            MessageBox.Show(
                "I am a managed app.\n\n" +
                "I am running inside: [" +
                System.Diagnostics.Process.GetCurrentProcess().ProcessName +
                "]\n\n" + (String.IsNullOrEmpty(pwzArgument) ?
                "I was not given an argument" :
                "I was given this argument: [" + pwzArgument + "]"));

            return 0;
        }

        

        static void Main(string[] args)
        {
            EntryPoint("hello world");
        }

        /*
        ICLRRuntimeHost::ExecuteInDefaultAppDomain. Valid .NET methods must have the following signature:
                static int pwzMethodName (String pwzArgument);
        As a side note, access modifiers such as public, protected, private, and internal do not affect
        the visibility of the method; therefore, they have been excluded from the signature. 
        */

        static int Xest(String pwzArgument)
        {
            // The console operation doesn't work!
            //Console.WriteLine("Hello {} - from staged Assembly!", pwzArgument);
            return 1337;
        }


    }
}
