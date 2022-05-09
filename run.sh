#!/bin/bash 

touch "status.txt"
echo $(date) >> status.txt
for i in {1..2}
do
    # We want to run both tests, and then move the generated data to the appropriate folders
    cd VariantA
    python3 search.py
    status=$?
    cd ../
    mv "VariantA/generational_fitness.npy" "test_data/${i}_A_gen_fitness.npy"
    mv "VariantA/final_positions.npy" "test_data/${i}_A_final_positions.npy"
    mv "VariantA/best_controller.npy" "test_data/${i}_A_best_controller.npy"
    comp_time=$(date)
    echo "Run ${i}, variant A done ${status}, ${comp_time}" >> "status.txt"

    cd VariantB 
    python3 search.py
    status=$?
    cd ../
    mv "VariantB/generational_fitness.npy" "test_data/${i}_B_gen_fitness.npy"
    mv "VariantB/final_positions.npy" "test_data/${i}_B_final_positions.npy"
    mv "VariantB/best_controller_STH.npy" "test_data/${i}_B_best_controller_STH.npy"
    mv "VariantB/best_controller_HTM.npy" "test_data/${i}_B_best_controller_HTM.npy"
    comp_time=$(date)
    echo "Run ${i}, variant B done ${status}, ${comp_time}" >> "status.txt"
done 
echo $(date) >> status.txt 
