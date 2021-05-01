using JuMP, Gurobi

test = "cmb05"

struct Instance
    v :: Int64 # Number of nodes
    E          # Array of tuples representing the edges
    k :: Int64 # Number of colours
    W          # Weight of each node

    function Instance(filepath)
        open(filepath) do file

            ##### FIRST     LINE  #####
            line = split(readline(file)," ")
            v = parse(Int64,line[1])
            numEdges = parse(Int64,line[2])
            k = parse(Int64,line[3])

            ##### SECOND    LINE  #####
            line = split(readline(file)," ")
            W = zeros(v)
            for i=1:v
                W[i] = parse(Float64,line[i])
            end

            ##### REMAINING LINES #####
            lines = readlines(file)
            E = Array{Tuple{Int, Int}}(undef, numEdges)
            for i=1:numEdges
                if(line != "" && line != " ")
                    line = split(lines[i], " ")
                    E[i]=(parse(Int64,line[1])+1,parse(Int64,line[2])+1) # Adds 1 to compensate the fact that Julia starts arrays in 1
                end
            end
            # Initializes the structure
            new(v,E,k,W)
        end
    end
end

inst = Instance(string("instances/", test))

struct SolverSolution
    X
    C
    m :: Int64
    function SolverSolution(instance)
        X = zeros(instance.v,instance.k)
        C = zeros(instance.k)
        k = instance.k
        K = collect(1:k)
        v = instance.v
        V = collect(1:v)

        model = Model(Gurobi.Optimizer)
        set_optimizer_attribute(model, "LogFile", string(test, " log.txt"))
        @variable(model, 0 <= m)
        @variable(model, X[V,K], Bin)
        @variable(model, 0 <= C[K])
        @objective(model, Min, m)
        for i in V
            @constraint(model, sum(X[i,a] for a in K)==1)
        end
        for a in K
            @constraint(model, sum(X[i,a]*instance.W[i] for i in V)==C[a])
            @constraint(model, m>=C[a])
        end
        for edge in instance.E
            i = edge[1]
            j = edge[2]
            for a in K
                @constraint(model,X[i,a]+X[j,a]<=1)
            end
        end
        print("Model complete. Solving...")
        optimize!(model)
        println("Solved.")
    end
end

SolverSolution(inst)

