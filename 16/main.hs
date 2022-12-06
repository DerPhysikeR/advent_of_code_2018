{-# LANGUAGE OverloadedStrings #-}
import Data.Text (Text(..), splitOn, unpack, strip)
import Data.Text.IO qualified as IO
import Data.Sequence (Seq(..), fromList, update, index)
import Data.Bits ((.&.), (.|.))
import Data.Map (Map(..), lookup, empty)
import Data.Map qualified as M
import Data.Set qualified as S
import Control.Monad (foldM)

type Register = Seq Int
type Opcode = Int
type InsOut = (Int, Int, Int)
type Instruction = (Opcode, InsOut)
type Operation = InsOut -> Register -> Register
type Example = (Register, Instruction, Register)
type FunctionMap = Map Int Operation
type FunctionIndexMap = Map Int Int

addr :: Operation
addr (a, b, c) r = update c (index r a + index r b) r
addi (a, b, c) r = update c (index r a + b) r
mulr (a, b, c) r = update c (index r a * index r b) r
muli (a, b, c) r = update c (index r a * b) r
banr (a, b, c) r = update c (index r a .&. index r b) r
bani (a, b, c) r = update c (index r a .&. b) r
borr (a, b, c) r = update c (index r a .|. index r b) r
bori (a, b, c) r = update c (index r a .|. b) r
setr (a, b, c) r = update c (index r a) r
seti (a, b, c) = update c a
gtir (a, b, c) r = update c (if a > index r b then 1 else 0) r
gtri (a, b, c) r = update c (if index r a > b then 1 else 0) r
gtrr (a, b, c) r = update c (if index r a > index r b then 1 else 0) r
eqir (a, b, c) r = update c (if a == index r b then 1 else 0) r
eqri (a, b, c) r = update c (if index r a == b then 1 else 0) r
eqrr (a, b, c) r = update c (if index r a == index r b then 1 else 0) r

functions :: [Operation]
functions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

parseExample :: Text -> Example
parseExample t = (beforeRegister, (opcode, (a, b, c)), afterRegister)
    where (before:middle:after:_) = splitOn "\n" t
          parseRegister = fromList . read . unpack . last . splitOn ": "
          beforeRegister = parseRegister before
          afterRegister = parseRegister after
          (opcode:a:b:c:_) = map (read . unpack ) (splitOn " " middle)

parseInput :: Text -> ([Example], [Instruction])
parseInput text = (map parseExample (splitOn "\n\n" firstPart), program)
    where (firstPart:secondPart:_) = splitOn "\n\n\n\n" text
          program = map parseInstruction (splitOn "\n" (strip secondPart))

parseInstruction :: Text -> Instruction
parseInstruction t = (opcode, (a, b, c))
    where (opcode:a:b:c:_) = map (read . unpack) (splitOn " " t)

howManyFunctionsFitExample :: Example -> Int
howManyFunctionsFitExample e = sum $ fmap (fromEnum . fitsExample e) functions

fitsExample :: Example -> Operation -> Bool
fitsExample (input, (_, insOut), output) fun = fun insOut input == output

runInstruction :: FunctionMap -> Register -> Instruction -> Maybe Register
runInstruction fm r (opcode, insOut) = case M.lookup opcode fm of
        Nothing -> Nothing
        Just fun -> Just (fun insOut r)

run :: FunctionMap -> [Instruction] -> Maybe Register
run fm = foldM (runInstruction fm) (fromList [0, 0, 0, 0])

findFunctionIndexMap :: Map Int (S.Set Int) -> FunctionIndexMap -> FunctionIndexMap
findFunctionIndexMap opm fim
    | M.null opm = fim
    | otherwise = findFunctionIndexMap newOpm newFim
        where uniqueFunctions = filter (\(_, funIdxSet) -> S.size funIdxSet == 1) (M.toList opm)
              newFim = foldr (\(opcode, funIdxSet) acc -> M.insert opcode (head $ S.toList funIdxSet) acc) fim uniqueFunctions
              uniqueFunctionIdxs = S.fromList [head $ S.toList idx | (_, idx) <- uniqueFunctions]
              removedFunctionIdxs = [(opcode, S.difference funIdxSet uniqueFunctionIdxs) | (opcode, funIdxSet) <- M.toList opm]
              newOpm = (M.fromList . filter (\(_, s) -> not $ S.null s)) removedFunctionIdxs

enumerate = zip [0..]

main :: IO ()
main = do
    (examples, program) <- parseInput <$> IO.readFile "input.txt"
    print $ sum $ map (fromEnum . (>=3) . howManyFunctionsFitExample) examples
    let allOpcodesAllFunctions = concat [[(opcode, idx) | (idx, fun) <- enumerate functions, fun insOut input == output] | e@(input, (opcode, insOut), output) <- examples]
    let allOpcodesAllFunctionsMap = foldr (\(opcode, idx) acc -> M.insertWith S.union opcode (S.singleton idx) acc) empty allOpcodesAllFunctions
    let functionIndexMap = findFunctionIndexMap allOpcodesAllFunctionsMap M.empty
    let functionMap = M.fromList [(opcode, functions!!funIdx) | (opcode, funIdx) <- M.toList functionIndexMap]
    print $ run functionMap program
