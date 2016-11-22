(defn avg [lo hi] (+ lo (/ (- hi lo) 2)))


(defn bisect-left
  "Returns the leftmost index at which x can be inserted
  into the sorted vector v."
  [v x]
  (loop [lo 0 hi (count v)]
    ;; Loop invariants:
    ;;   - everything to the left of lo is < x
    ;;   - everything at or to the right of hi is >= x
    ;; In the end, lo == hi and lo is the leftmost spot that is >= x.
    (let [mid (int (avg lo hi))]
      (cond
        (= lo hi) lo
        (< (get v mid) x) (recur (inc mid) hi)
        :else (recur lo mid)))))


(defn bisect-right
  "Returns the rightmost index at which x can be inserted
  into the sorted vector v."
  [v x]
  (loop [lo 0 hi (count v)]
    ;; Loop invariants:
    ;;   - everything to the left of lo is <= x
    ;;   - everything at or to the right of hi is > x
    ;; In the end, lo == hi and lo is the leftmost spot that is > x.
    (let [mid (int (avg lo hi))]
      (cond
        (= lo hi) lo
        (> (get v mid) x) (recur lo mid)
        :else (recur (inc mid) hi)))))
