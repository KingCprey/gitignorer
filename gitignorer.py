#!/usr/bin/env python3
import argparse,requests,os,sys
#possibly detect whether cwd is inside a git repo, then set .gitignore
DOWNLOAD_LOCATION="https://raw.githubusercontent.com/github/gitignore/master/%s"

#def get_gitignore_list(ignore_location=GITIGNORE_LOCATION):
def yesno(prompt,default=False,confirm=["y","yes","ya","aye"],deny=["n","no","pissoff"]):
    c=[y.lower() for y in confirm]
    d=[n.lower() for n in deny]
    a=input(prompt)
    if a in confirm:return True
    elif a in deny:return False
    else:return default

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-o","--output",help="The output location (file path, [stdout], stderr)",action="store")
    parser.add_argument("-f","--force",action="store_true",help="If file exists at output location")
    parser.add_argument("-v","--verbose",action="store_true",help="Get that verbosity going boah")
    parser.add_argument("toignore",help="The .gitignore file to grab")
    parsed=parser.parse_args()
    if parsed.verbose:print(parsed)
    toignore=parsed.toignore.title() #the files are capitalised and Github files are case sensitive
    fname,ext=os.path.splitext(toignore)
    toignore=fname+".gitignore"
    r=requests.get(DOWNLOAD_LOCATION%toignore)
    if r.status_code==200:
        if not parsed.output is None:
            if parsed.output.lower() in ["stdin","stderr"]:
                if parsed.output.lower()=="stdin":print(r.text,end='')
                else:print(r.text,file=sys.stderr,end='')
            else:
                if os.path.exists(parsed.output):
                    if not parsed.force:
                        do_overwrite=yesno("File exists at %s, overwrite? y/n [N]: "%parsed.output)
                        if not do_overwrite:return
                with open(parsed.output,'wb')as output:
                    output.write(r.content)
        else:
            print(r.text,end='')
    elif r.status_code==404:
        raise FileNotFoundError("Couldn't download a .gitignore file at {0}".format(DOWNLOAD_LOCATION%toignore))
if __name__=="__main__":
    main()
