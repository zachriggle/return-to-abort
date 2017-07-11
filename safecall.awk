BEGIN{FS="\t"}
{
    print;
    if ($2 == "call" || $2 == "callq") {
        print("\t.byte 0xeb, 0x02, 0xfe, 0xca");
    }
}
