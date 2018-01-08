def main():
    with open('temp.txt') as infile:
        for line in infile:
            line = line.replace('#', '\#' )
            line = line.replace('%', '\%' )
            line = line.replace('@', '\@' )
            line = line.replace('$', '\$' )
            print(line, end='')

if __name__ == '__main__':
    main()
