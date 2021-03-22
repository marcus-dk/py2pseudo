# Py2Pseudo the official Python-2-Pseudocode Translator
# Py2Pseudo is developed and brought to you by:
# Marcus Sorensen - https://github.com/marcus-dk 
# Igor Michalec - https://github.com/BlueComrade

# Importing necessary modules
import re

# File name initialisation
python_file = 'file.py' # Name of the file to translate
pseudo_file = None

# Stack setup 
stack = []
def_stack = []

# Conversion Rules
basic_conversion = {"list":'"ARRAY',"raise":"RAISE","range":"RANGE","False":"FALSE","True":"TRUE","bool":'"BOOLEAN',"str":'"STRING',"float":'"REAL',"int":'"INTEGER',"continue":"CONTINUE","break":"BREAK"
                    ,"len":" LENGTH","print": '"SEND', "return": "RETURN", "input": "RECEIVE","import": "IMPORT", "else:": "ELSE", "elif": "ELSEIF","and":"AND","or":"OR","not":"NOT","except": "EXCEPT", "pass": "PASS", "in": "IN"}
stack_conversion = {'for"EACH': ["FOR EACH","END FOREACH"],"for": ["FOR","END FOR"],"if": ["IF","END IF","ELSE","ELSEIF"],"while": ["WHILE","END WHILE"], "until": ["UNTIL","END UNTIL"]
,"class": ["DEFINE CLASS","END CLASS"], "def": ["PROCEDURE","END PROCEDURE"], "try": ["TRY","END TRY","EXCEPT"]}
prefix_conversion = {"+=":"SET","-=":"SET","*=":"SET","/=":"SET","**=":"SET","=": "SET", "#F": "CALL "}
data_type_list = ['"ARRAY','"BOOLEAN','"STRING','"REAL','"INTEGER']
advanced_conversion = {"^":"XOR","**":"^","%":"MOD","//":"DIV","+=":"TO","-=":"TO","*=":"TO","^=":"TO","/=":"TO","**=":"TO","!=":"<>","=": "TO","==":"="}
quickswitch = {"^":"XOR","**":"^"}
peculiar_list = ["+=","*=","**=","-=","/=","^="]
equal_chars = ["!","=","*","/","<",">"]
front_chars = ["-","+"]
suffix_conversion = {"WHILE":" DO","FOR EACH":" DO","FOR":" DO","IF":" THEN","ELSEIF":" THEN","PROCEDURE":"","TRY":"","EXCEPT":"","DEFINE CLASS":""}
stop_chars = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0987654321_" # If any of these are next to a key word you do not read unless = or == 
input_name_counter = 0

# --------- Initialisation is completed, translation logic starts ---------

def list2pseudo(to_pseudo):

    to_pseudo.append(" ")
    list_add = []
    replace_list = []
    current_skip_char = ""
    line_index = -1
    input_name_counter = 0

    for line in to_pseudo:

        line_index = line_index + 1 + to_pseudo[line_index+1:].index(line) # if lines are the same
        line = str(line).replace("  ","\t")
        break_list = [] # takes out comments and strings
        replace_list = []
        i = 0
        char_to_use = "'"

        if current_skip_char != "":
            break_list.append(0)

        while i < len(line): # while loop because of double skips

            if current_skip_char == "":

                if line[i:i+3] == "'''":
                    break_list.append(i)
                    current_skip_char = "'''"
                    i += 2

                elif line[i:i+3] == '"""':
                    break_list.append(i)
                    current_skip_char = '"""'
                    i += 2

                elif line[i] == "'":
                    break_list.append(i)
                    current_skip_char = "'"

                elif line[i] == '"':
                    break_list.append(i)
                    current_skip_char = '"'

                elif line[i] == "#":
                    break_list.append(i)
                    char_to_use = '"'
                    break

            else:

                if line[i:i+len(current_skip_char)] == current_skip_char:
                    break_list.append(i+len(current_skip_char))
                    i += len(current_skip_char)-1
                    current_skip_char = ""

            i += 1

        if len(break_list) % 2 == 1:

            temp_take_of = break_list.pop()
            replace_list.append(line[temp_take_of:])
            line = line[:temp_take_of] + char_to_use
            char_to_use = "'"

        for i in range(len(break_list)-1,-1,-2):

            replace_list.append(line[break_list[i-1]:break_list[i]])
            line = line[:break_list[i-1]] + char_to_use + line[break_list[i]:]

        line = re.split(r'(\s+)', line)

        for key, value in prefix_conversion.items():

            count = 0

            for word in line:

                if key in word:

                    start = str(word).find(key)

                    if start == 0:
                        first = " "
                    else:
                        first = word[start-1]

                    if start+len(key) == len(word):
                        last = " "
                    else:
                        last = word[start+len(key)]

                    if True != (last in equal_chars or first in front_chars or first in equal_chars):

                        n_p_c = True

                        try:
                            escape = False
                            for i in range(count,-1,-1):

                                if i == count:
                                    j_use = start
                                else:
                                    j_use = len(line[i])-1
                                for j in range(j_use,-1,-1):
                                    if line[i][j] in "(){}[]":
                                        raise Exception

                        except:
                            n_p_c = False

                        if n_p_c:

                            if not str(line[0]) == '':
                                line[0] = value + " " + line[0]
                            else:
                                line[2] = value + " " + line[2]

                count += 1

        for key, value in basic_conversion.items():

            for e in range(len(line)):

                look_at = 0
                continues = True

                while continues:

                    if key in str(line[e][look_at:]):

                        start = str(line[e][look_at:]).find(key)

                        if start == 0:
                            first = " "
                        else:
                            first = line[e][look_at:][start-1]

                        if start + len(key) == len(line[e][look_at:]):
                            last = " "
                        else:
                            last = line[e][look_at:][start + len(key)]

                        if True != (last in stop_chars or first in stop_chars):

                            line[e] = line[e][:look_at]+line[e][look_at:].replace(key,value,1)
                            continues = True

                            if value in suffix_conversion.keys():

                                try:
                                    for i in range(len(line)-1,-1,-1):

                                        for j in range(len(line[i])-1,-1,-1):

                                            if line[i][j] in "(){}[]":
                                                raise Exception

                                            elif line[i][j] == ':':

                                                if j < len(line[i]):
                                                    line[i] = line[i][:j]+suffix_conversion[value]+line[i][j+1:]
                                                else:
                                                    line[i] = line[i][:j]+suffix_conversion[value]

                                                raise Exception

                                except:
                                    "needs to be here because try except"
                        else:
                            look_at += start + len(key)

                        if start + len(key) == len(line[e][look_at:]):
                            continues = False
                    else:
                        continues = False

        if len(line) != 1:

            if (line[0] == '' and  line[2] == '"'):
                cmd = ""
                num_of_t = len(stack)

            elif line[0] == "" and "\t" in line[1]:
                num_of_t = len(line[1])

            elif line[1] == "\n": # chars that work in python
                num_of_t = len(stack)

            else:
                num_of_t = 0

            if not str(line[0]) == '':
                cmd = line[0]
            else:
                cmd = line[2]

        else: # in case there is just one word
            if line == ['']:
                cmd = ""
                num_of_t = len(stack)

            elif line[0] == '"':
                cmd = ""
                num_of_t = len(stack)

            else: # ignore empty lines
                cmd = ""
                num_of_t = 0
        
        if len(stack) > num_of_t:

            while len(stack) > num_of_t:

                key = stack.pop()

                if key == "def":

                    full = def_stack.pop()
                    index = full[0]
                    list_a = full[1]
                    pro = full[2]
                    
                    if pro:

                        to_pseudo[index] = to_pseudo[index].replace("PROCEDURE","FUNCTION")
                        pro = False
                        list_add.append([line_index,len(stack)*"\t"+"END FUNCTION"+"\n"])
                        list_add[list_a][1] = list_add[list_a][1].replace("PROCEDURE","FUNCTION")
                        break

                    else:
                        list_add.append([line_index, len(stack) * "\t" + stack_conversion[key][1] + "\n"])
                
                elif (len(stack) == num_of_t) and (cmd in stack_conversion[key][2:]):
                    stack.append(key)
                    break

                else:
                    list_add.append([line_index, len(stack) * "\t" + stack_conversion[key][1] + "\n"])

        line = "".join(line)
        look_for = ""
        look_at = 0
        continues = True

        while continues:

            if "for" in str(line[look_at:]):
                look_for = "for"
                next_p = True

            elif '"SEND' in str(line[look_at:]):
                look_for = '"SEND'
                next_p = True

            else:
                next_p = False
                continues = False

            if next_p:

                start = line[look_at:].find(look_for)

                if start == 0:
                    first = " "
                else:
                    first = line[look_at:][start-1]

                if start+len(look_for) == len(line):
                    last = " "
                    start_index = -1
                else:
                    last = line[look_at:][start+len(look_for)]
                    start_index = start+len(look_for)

                if True != (last in stop_chars or first in stop_chars):
                    if start_index != -1:

                        stack_of_exceptions = []

                        if look_for == "for":

                            in_found =False
                            look_at2 = 0

                            while not in_found:

                                start2 = line[look_at+look_at2+start_index:].find("IN")

                                if start2 == 0:
                                    first2 = " "
                                else:
                                    first2 = line[look_at+look_at2+start_index:][start2-1]

                                if start+len("IN") == len(line):
                                    last2 = " "
                                    start_index2 = -1
                                else:
                                    last2 = line[look_at+look_at2+start_index:][start2+len("IN")]
                                    start_index2 = start2+len("IN")

                                if True != (last2 in stop_chars or first2 in stop_chars):
                                    in_found = True
                                else:
                                    look_at2+=start2+len("IN")

                            if start_index2!= -1:

                                begin = look_at2+start_index+look_at+start_index2
                                range_found = False
                                coords = -1

                                for i in range(begin,len(line)):

                                    if line[i] in "({[]})":
                                        break

                                    else:
                                        if line[i:i+5] == "RANGE":
                                            out = False
                                            if i+5!=len(line):
                                                out = True
                                            if ((out ==-1) or line[i+5] not in stop_chars) and (line[i-1] not in stop_chars):
                                                range_found = True
                                                coords = i+5
                                            break

                                if range_found:

                                    look_B = False
                                    separate_by = []

                                    for i in range(coords,len(line)):

                                        if line[i] in "({[":

                                            if stack_of_exceptions == []:
                                                index_start_B = i+1
                                            stack_of_exceptions.append(line[i])

                                        elif line[i] in "]})":
                                            stack_of_exceptions.pop()

                                        if stack_of_exceptions == ["("]:
                                            if line[i]==",":
                                                separate_by.append(i)
                                            look_B = True

                                        if look_B and stack_of_exceptions == []:
                                            index_B = i
                                            break

                                    inside = ['0','TO','0','STEP','1']

                                    if len(separate_by) == 0:
                                        inside[2] = line[index_start_B:index_B]

                                    elif len(separate_by) == 1:
                                        inside[0] = line[index_start_B:separate_by[0]]
                                        inside[2] = line[separate_by[0]+1:index_B]

                                    else:
                                        inside[0] = line[index_start_B:separate_by[0]]
                                        inside[2] = line[separate_by[0]+1:separate_by[1]]
                                        inside[4] = line[separate_by[1]+1:index_B]

                                    line = line[:coords-5]+" ".join(inside)+line[index_B+1:]
                                    line = line[:look_at+look_at2+start_index+start2]+" FROM "+line[look_at+look_at2+start_index+start_index2:]

                                else:
                                    line = line[:look_at+look_at2+start_index+start2]+" FROM "+line[look_at+look_at2+start_index+start_index2:]
                                    line = line[:start_index]+'"EACH'+line[start_index:]

                        elif look_for == '"SEND':

                            look_B = False
                            n_p_for_brackets = False

                            for i in range(start_index+look_at,len(line)):

                                if line[i] in "({[":

                                    if stack_of_exceptions == []:
                                        index_start_B = i
                                        n_p_for_brackets = True
                                    stack_of_exceptions.append(line[i])

                                elif line[i] in "]})":
                                    stack_of_exceptions.pop()

                                if stack_of_exceptions == ["("]:
                                    look_B = True

                                if look_B and stack_of_exceptions == []:
                                    index_B = i
                                    break

                            if n_p_for_brackets:
                                line = line[:index_start_B]+" " + line[index_start_B+1:]
                                line = line[:index_B]+" TO DISPLAY " + line[index_B+1:]
                            line = line[:start_index+look_at-5]+line[start_index+look_at-4:]

                    else:
                        continues = False

                look_at += start+len(look_for)

        line = re.split(r'(\s+)', line)
        temp = ""

        for key, value in stack_conversion.items():

            for e in range(len(line)):

                look_at = 0
                continues = True

                while continues:

                    if key in str(line[e][look_at:]):

                        start = str(line[e][look_at:]).find(key)

                        if start == 0:
                            first = " "
                        else:
                            first = line[e][look_at:][start-1]

                        if start+len(key) == len(line[e][look_at:]):
                            last = " "
                        else:
                            last = line[e][look_at:][start+len(key)]

                        if True != (last in stop_chars or first in stop_chars):

                            continues = True

                            if key == "def":
                                num = len(list_add)
                                list_add.append([line_index+1,len(stack)*"\t"+"BEGIN PROCEDURE\n"])
                                def_stack.append([line_index,num,False])

                            line[e] = line[e][:look_at]+ line[e][look_at:].replace(key,value[0],1)

                            if value[0] in suffix_conversion.keys():

                                try:
                                    for i in range(len(line)-1,-1,-1):

                                        for j in range(len(line[i])-1,-1,-1):

                                            if line[i][j] in "(){}[]":
                                                raise Exception

                                            elif line[i][j] == ':':
                                                stack.append(key)

                                                if j < len(line[i]):
                                                    line[i] = line[i][:j]+suffix_conversion[value[0]]+line[i][j+1:]
                                                else:
                                                    line[i] = line[i][:j]+suffix_conversion[value[0]]
                                                raise Exception
                                
                                except:
                                    "needs to be here because try except"

                        else:
                            look_at += start+len(key)

                        if start+len(key) == len(line[e][look_at:]):
                            continues = False

                    else:
                            continues = False

        for key, value in advanced_conversion.items():

            for e in range(len(line)):

                look_at = 0
                continues = True

                while continues:

                    if key in str(line[e][look_at:]):

                        start = str(line[e][look_at:]).find(key)

                        if start == 0:
                            first = " "
                        else:
                            first = line[e][look_at:][start-1]

                        if start+len(key) == len(line[e][look_at:]):
                            last = " "
                        else:
                            last = line[e][look_at:][start+len(key)]

                        if True != (last in equal_chars or first in front_chars or first in equal_chars):

                            line[e] =  line[e][:look_at]+ line[e][look_at:].replace(key," "+value+" ",1)

                            if key in peculiar_list:

                                use_key = key[:-1]

                                if use_key in quickswitch.keys():
                                    use_key = quickswitch[use_key]
                                if start ==0:
                                    line[e] = line[e][:start+len(value)+2]+" "+line[e-2]+" "+use_key+" "+line[e][start+len(value)+2:]
                                else:
                                    line[e] = line[e][:start+len(value)+2]+" "+line[e][:start]+" "+use_key+" "+line[e][start+len(value)+2:]

                            continues = True

                        else:
                            look_at += start+len(key)

                        if start+len(key) == len(line[e][look_at:]):
                            continues = False

                    else:
                            continues = False

        for key, value in prefix_conversion.items():

            for word in line:

                if word == key:
                    del line[line.index(word)]

        line = "".join(line)

        def receiver(line,replace_list,add_print_n_receive,input_name_counter,og,self_r,tabs):

            i = 0

            while i <len(line):

                isnt_replaced = False

                for k in data_type_list:

                    if line[i:i+len(k)] == k:
                        isnt_replaced = True

                if (line[i] == '"'or line[i] == "'") and not isnt_replaced and not self_r:

                    line = line[:i]+replace_list[-1]+line[i+1:]
                    i+= len(replace_list[-1])-1
                    replace_list.pop()

                elif line[i:i+7] == "RECEIVE":

                    if (i == 0 or line[i-1] not in stop_chars) and (i+7 == len(line) or line[i+7] not in stop_chars):

                        temp_stack = []
                        bracket = True
                        start_stack = False

                        for j in range(i+7,len(line)):

                            if not(line[j:j+2] == "\t" or line[j-1:j+1] == "\t" or line[j]==" " or line[j]=="(") and not start_stack:
                                bracket = False
                                break

                            elif start_stack:

                                if line[j]=="(":
                                    temp_stack.append("(")
                                elif line[j]==")":
                                    temp_stack.pop()
                                if temp_stack == []:
                                    end = j+1
                                    break

                            elif line[j]=="(":
                                temp_stack.append("(")
                                start_stack = True
                                
                        if bracket:

                            index_of_add,add_print_n_receive,input_name_counter = receiver(line[i+7:end-1],replace_list,add_print_n_receive,input_name_counter,og,False,tabs)
                            only = True
                            start = -1

                            if i == 0 or end == len(line):
                                only = False

                            else:
                                for k in range(i-1,-1,-1):

                                    if k != 0:

                                        if line[k] == "(":
                                            start = k
                                            break
                                        elif not(line[k:k+2] == "\t" or line[k-1:k+1] == "\t" or line[k]==" " ):
                                            only = False
                                            break

                                    else:

                                        if line[k] == "(":
                                            start = k
                                            break
                                        elif not(line[k:k+2] == "\t" or line[k]==" " ):
                                            only = False
                                            break

                                for k in range(end,len(line)):

                                    if k != len(line)-1:
                                        if line[k] == ")":
                                            break
                                        elif not(line[k:k+2] == "\t" or line[k-1:k+1] == "\t" or line[k]==" " ):
                                            only = False
                                            break

                                    else:
                                        if line[k] == ")":
                                            break
                                        elif not(line[k-1:k+1] == "\t" or line[k]==" " ):
                                            only = False
                                            break

                            data_used = "STRING"
                            add_front =0
                            add_bottom = 0

                            if only and start>0:

                                for k in data_type_list:

                                    for m in range(start,-1,-1):

                                        if m-len(k) >=0:

                                            if line[m-len(k):m] == k:

                                                if m-len(k)-1<0 or line[m-len(k)-1] not in stop_chars:
                                                    data_used = k[1:]
                                                    add_front =len(k)+1
                                                    add_bottom = 1
                                                break

                                            elif not(line[m:m+2] == "\t" or line[m-1:m+1] == "\t" or line[m]==" " ):
                                                break

                                        else:
                                            break

                            add_print_n_receive.append("\t"*tabs+"RECEIVE temp_input_var_"+str(input_name_counter)+" FROM("+data_used+")KEYBOARD")
                            line = line[:i-add_front]+" temp_input_var_"+str(input_name_counter)+" "+line[add_bottom+end:]
                            i+=len(" temp_input_var_"+str(input_name_counter))-add_front
                            input_name_counter+=1

                        else:
                            i+=5

                    else:
                        i+=5

                i+=1

            for k in data_type_list:
                line = line.replace(k,k[1:])

            if self_r:
                return replace_list,add_print_n_receive,input_name_counter,line
            else:
                add_print_n_receive.append("\t"*tabs+"SEND "+line+" TO DISPLAY")
                return replace_list,add_print_n_receive,input_name_counter

        data_used = "STRING"

        if "RECEIVE" in line:

            cont_ = True

            if "TO" in line:

                if "SET" in line:
                    index = line.find("SET")

                    if not(((line[index-1] in equal_chars or line[index-1] in front_chars) and index !=0) or line[index+2] in equal_chars):

                        index = line.find("TO")

                        if not(line[index-1] in equal_chars or line[index-1] in front_chars or line[index+2] in equal_chars):

                            bracket = False
                            single = True
                            extra_b1 = False
                            extra_b2 = False
                            stack_for_receive = []
                            i = index + 2

                            while i <len(line):

                                for k in data_type_list:

                                    if i+len(k) <len(line):

                                        if line[i:i+len(k)] == k:
                                            i+=len(k)
                                            extra_b1 = True
                                            extra_b2 = True
                                            data_used = k[1:]
                                            break

                                    else:
                                        break

                                if (line[i:i+8] == 'RECEIVE(' or bracket) and single:

                                    if (line[i:i+8] == 'RECEIVE(' and bracket!=True):
                                        start = i+8
                                        i+=7

                                    bracket = True

                                    if line[i] == '(':
                                        stack_for_receive.append("(")

                                    elif line[i] == ')':
                                        stack_for_receive.pop()

                                    if stack_for_receive == []:
                                        end = i
                                        bracket = False
                                        single = False

                                elif extra_b1 and line[i]=="(":
                                    extra_b1 = False

                                elif extra_b2 and line[i]==")":
                                    extra_b2 = False

                                elif not(line[i:i+2] == "\n" or line[i-1:i+1] == "\n" or line[i:i+2] == "\t" or line[i-1:i+1] == "\t" or line[i]==" " or line[i] =='"'):
                                    cont_ = False
                                    break

                                i+=1
                        else:
                            cont_ = False
                    else:
                        cont_ = False
                else:
                    cont_ = False
            else:
                cont_ = False

            if cont_:
                index1 = line.find("SET")+3
                index2 = line.find("TO")
                name = line[index1:index2].replace("/t","").replace(" ","")

                replace_list,to_add,input_name_counter =receiver(line[start:end],replace_list,[],input_name_counter,len(replace_list),False,len(stack))

                for i in range(len(to_add)):
                    list_add.append([line_index,to_add[i]])

                if line[-1] ==  '"':
                    line = "\t"*len(stack)+"RECEIVE "+name+" FROM("+data_used+')KEYBOARD"'
                else:
                    line = "\t"*len(stack)+"RECEIVE "+name+" FROM("+data_used+')KEYBOARD'

            else:
                replace_list,to_add,input_name_counter,line =receiver(line,replace_list,[],input_name_counter,len(replace_list),True,len(stack))

                for i in range(len(to_add)):
                    list_add.append([line_index,to_add[i]])

        for k in data_type_list:
            line = line.replace(k,k[1:])
        if "RETURN" in line:
            def_stack[-1][2] = True

        to_pseudo[line_index] = line
        to_pseudo[line_index] = to_pseudo[line_index].replace('"',"'")
        to_pseudo[line_index] = to_pseudo[line_index].split("'")

        for i in range(len(replace_list)):
            to_pseudo[line_index].insert(len(replace_list)-i,replace_list[i])

        to_pseudo[line_index]= "".join(to_pseudo[line_index])

    for i in range(len(list_add)):
        to_pseudo.insert(list_add[i][0]+i,list_add[i][1])

    return(to_pseudo)


def pseudo2file(to_file):
    file = open("output.txt", 'w')

    for line in to_file:
        print(line, file=file)

def main():

    main_file = open(python_file, 'r+')
    pseudo_file = main_file.readlines()
    pseudo_file = list2pseudo(pseudo_file)
    pseudo2file(pseudo_file)

if __name__ == "__main__":
    main()
