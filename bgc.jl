struct Instance
    v :: Int64 # Number of nodes
    E          # Array of tuples representing the edges
    k :: Int64 # Number of colours
    W          # Weight of each node
    function Instance(filepath)
        open(filepath) do file
            line = split(readline(file)," ")
            v = parse(Int64,line[1])
            numEdges = parse(Int64,line[2])
            k = parse(Int64,line[3])
            line = split(readline(file)," ")
            W = zeros(v)
            for i=1:v
                W = parse(Float64,line[i])
            end
            lines = readlines(file)
            E = Array{Tuple{Int, Int}}(undef, first(size(lines)))
            for i=1:numEdges
                line = split(lines[i], " ")
                E[i]=(parse(Int64,line[1])+1,parse(Int64,line[2])+1) # Adds 1 to compensate the fact that Julia starts the arrays in 1 instead of 0
                i = i+1
            end
            new(v,E,k,W)
        end
    end
end

inst = Instance("instances/cmb01")

struct Solution
    X
    C
    m :: Int64
    function Solution(Instance)

    end
end

